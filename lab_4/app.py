import csv
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation
from tkinter import END, BOTH, LEFT, RIGHT, X, Y, Button, Entry, Frame, Label, Tk, messagebox, filedialog
from tkinter import ttk

import psycopg2
from psycopg2.extras import RealDictCursor


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "production_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}


class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учет изделий производства")
        self.root.geometry("1120x640")
        self.conn = None
        self.groups = {}
        self.selected_product_id = None

        self.connect()
        self.build_ui()
        self.load_groups()
        self.load_products()

    def connect(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
        except psycopg2.Error as error:
            messagebox.showerror(
                "Ошибка подключения",
                "Не удалось подключиться к PostgreSQL.\n\n"
                "Проверьте настройки DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD.\n\n"
                f"{error}",
            )
            raise

    def build_ui(self):
        main = Frame(self.root, padx=12, pady=12)
        main.pack(fill=BOTH, expand=True)

        form = Frame(main)
        form.pack(side=LEFT, fill=Y, padx=(0, 12))

        table_area = Frame(main)
        table_area.pack(side=RIGHT, fill=BOTH, expand=True)

        Label(form, text="Данные изделия").pack(anchor="w")

        self.product_code = self.add_input(form, "Обозначение изделия")
        self.group_box = self.add_combobox(form, "Группа")
        self.release_year = self.add_input(form, "Год выпуска")
        self.output_volume = self.add_input(form, "Объем выпуска")
        self.metal_consumption = self.add_input(form, "Расход металла")
        self.note = self.add_input(form, "Примечание")

        Button(form, text="Добавить изделие", command=self.add_product).pack(fill=X, pady=(14, 4))
        Button(form, text="Изменить изделие", command=self.update_product).pack(fill=X, pady=4)
        Button(form, text="Удалить изделие", command=self.delete_product).pack(fill=X, pady=4)
        Button(form, text="Очистить поля", command=self.clear_form).pack(fill=X, pady=4)

        Label(form, text="Поиск").pack(anchor="w", pady=(18, 0))
        self.search_text = self.add_input(form, "Код или год")
        Button(form, text="Найти по коду или году", command=self.search_products).pack(fill=X, pady=(10, 4))
        Button(form, text="Найти по группе", command=self.search_by_group).pack(fill=X, pady=4)
        Button(form, text="Показать все", command=self.load_products).pack(fill=X, pady=4)
        Button(form, text="Сформировать отчет", command=self.export_report).pack(fill=X, pady=(18, 4))

        columns = (
            "product_id",
            "product_code",
            "group_name",
            "release_year",
            "output_volume",
            "metal_consumption",
            "note",
        )
        self.tree = ttk.Treeview(table_area, columns=columns, show="headings", height=24)
        self.tree.heading("product_id", text="ID")
        self.tree.heading("product_code", text="Обозначение")
        self.tree.heading("group_name", text="Группа")
        self.tree.heading("release_year", text="Год")
        self.tree.heading("output_volume", text="Объем")
        self.tree.heading("metal_consumption", text="Металл")
        self.tree.heading("note", text="Примечание")

        self.tree.column("product_id", width=60, anchor="center")
        self.tree.column("product_code", width=140)
        self.tree.column("group_name", width=180)
        self.tree.column("release_year", width=80, anchor="center")
        self.tree.column("output_volume", width=100, anchor="e")
        self.tree.column("metal_consumption", width=100, anchor="e")
        self.tree.column("note", width=260)

        scrollbar = ttk.Scrollbar(table_area, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def add_input(self, parent, label):
        Label(parent, text=label).pack(anchor="w", pady=(8, 0))
        entry = Entry(parent, width=32)
        entry.pack(fill=X)
        return entry

    def add_combobox(self, parent, label):
        Label(parent, text=label).pack(anchor="w", pady=(8, 0))
        combo = ttk.Combobox(parent, width=30, state="readonly")
        combo.pack(fill=X)
        return combo

    def load_groups(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT group_id, group_name FROM product_groups ORDER BY group_name")
            rows = cur.fetchall()
        self.groups = {row["group_name"]: row["group_id"] for row in rows}
        self.group_box["values"] = list(self.groups.keys())
        if rows and not self.group_box.get():
            self.group_box.current(0)

    def load_products(self):
        query = """
            SELECT
                p.product_id,
                p.product_code,
                g.group_name,
                p.release_year,
                p.output_volume,
                p.metal_consumption,
                COALESCE(p.note, '') AS note
            FROM products p
            JOIN product_groups g ON g.group_id = p.group_id
            ORDER BY p.product_id;
        """
        self.fill_table(self.fetch_all(query))

    def search_products(self):
        value = self.search_text.get().strip()
        if not value:
            self.load_products()
            return

        params = {"code": value}
        where = "p.product_code = %(code)s"
        if value.isdigit():
            params["year"] = int(value)
            where = f"({where} OR p.release_year = %(year)s)"

        query = f"""
            SELECT
                p.product_id,
                p.product_code,
                g.group_name,
                p.release_year,
                p.output_volume,
                p.metal_consumption,
                COALESCE(p.note, '') AS note
            FROM products p
            JOIN product_groups g ON g.group_id = p.group_id
            WHERE {where}
            ORDER BY p.product_id;
        """
        self.fill_table(self.fetch_all(query, params))

    def search_by_group(self):
        group_name = self.group_box.get().strip()
        if group_name not in self.groups:
            messagebox.showwarning("Поиск", "Выберите группу из справочника.")
            return

        query = """
            SELECT
                p.product_id,
                p.product_code,
                g.group_name,
                p.release_year,
                p.output_volume,
                p.metal_consumption,
                COALESCE(p.note, '') AS note
            FROM products p
            JOIN product_groups g ON g.group_id = p.group_id
            WHERE p.group_id = %(group_id)s
            ORDER BY p.product_id;
        """
        self.fill_table(self.fetch_all(query, {"group_id": self.groups[group_name]}))

    def add_product(self):
        values = self.read_form()
        if values is None:
            return

        query = """
            INSERT INTO products (
                product_code,
                group_id,
                release_year,
                output_volume,
                metal_consumption,
                note
            )
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        if not self.execute_query(query, values):
            return
        self.load_products()
        self.clear_form()
        messagebox.showinfo("Готово", "Изделие добавлено.")

    def update_product(self):
        if not self.selected_product_id:
            messagebox.showwarning("Выбор записи", "Выберите изделие в таблице.")
            return

        values = self.read_form()
        if values is None:
            return

        query = """
            UPDATE products
            SET product_code = %s,
                group_id = %s,
                release_year = %s,
                output_volume = %s,
                metal_consumption = %s,
                note = %s
            WHERE product_id = %s;
        """
        if not self.execute_query(query, (*values, self.selected_product_id)):
            return
        self.load_products()
        messagebox.showinfo("Готово", "Изделие изменено.")

    def delete_product(self):
        if not self.selected_product_id:
            messagebox.showwarning("Выбор записи", "Выберите изделие в таблице.")
            return
        if not messagebox.askyesno("Удаление", "Удалить выбранное изделие?"):
            return

        if not self.execute_query("DELETE FROM products WHERE product_id = %s;", (self.selected_product_id,)):
            return
        self.load_products()
        self.clear_form()
        messagebox.showinfo("Готово", "Изделие удалено.")

    def export_report(self):
        rows = self.get_table_rows()
        if not rows:
            messagebox.showwarning("Отчет", "Нет данных для отчета.")
            return

        default_name = f"products_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        path = filedialog.asksaveasfilename(
            title="Сохранить отчет",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=(("CSV files", "*.csv"), ("Text files", "*.txt")),
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["ID", "Обозначение", "Группа", "Год", "Объем", "Расход металла", "Примечание"])
            writer.writerows(rows)

        messagebox.showinfo("Отчет", f"Отчет сохранен:\n{path}")

    def read_form(self):
        code = self.product_code.get().strip()
        group_name = self.group_box.get().strip()
        year = self.release_year.get().strip()
        volume = self.output_volume.get().strip()
        metal = self.metal_consumption.get().strip().replace(",", ".")
        note = self.note.get().strip() or None

        if not code or not group_name or not year or not volume or not metal:
            messagebox.showwarning("Проверка данных", "Заполните все обязательные поля.")
            return None

        try:
            year_value = int(year)
            volume_value = int(volume)
            metal_value = Decimal(metal)
        except (ValueError, InvalidOperation):
            messagebox.showwarning("Проверка данных", "Год, объем и расход металла должны быть числами.")
            return None

        if group_name not in self.groups:
            messagebox.showwarning("Проверка данных", "Выберите группу из справочника.")
            return None

        return code, self.groups[group_name], year_value, volume_value, metal_value, note

    def on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_product_id = int(values[0])
        self.set_entry(self.product_code, values[1])
        self.group_box.set(values[2])
        self.set_entry(self.release_year, values[3])
        self.set_entry(self.output_volume, values[4])
        self.set_entry(self.metal_consumption, values[5])
        self.set_entry(self.note, values[6])

    def clear_form(self):
        self.selected_product_id = None
        for entry in (
            self.product_code,
            self.release_year,
            self.output_volume,
            self.metal_consumption,
            self.note,
            self.search_text,
        ):
            entry.delete(0, END)
        if self.group_box["values"]:
            self.group_box.current(0)
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def fill_table(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            self.tree.insert(
                "",
                END,
                values=(
                    row["product_id"],
                    row["product_code"],
                    row["group_name"],
                    row["release_year"],
                    row["output_volume"],
                    row["metal_consumption"],
                    row["note"],
                ),
            )

    def get_table_rows(self):
        return [self.tree.item(item, "values") for item in self.tree.get_children()]

    def set_entry(self, entry, value):
        entry.delete(0, END)
        entry.insert(0, value)

    def fetch_all(self, query, params=None):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def execute_query(self, query, params):
        try:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
            self.conn.commit()
            return True
        except psycopg2.Error as error:
            self.conn.rollback()
            messagebox.showerror("Ошибка SQL", str(error))
            return False

    def close(self):
        if self.conn:
            self.conn.close()


def main():
    root = Tk()
    app = ProductApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.close(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()
