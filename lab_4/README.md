# Лабораторная работа: база данных "Производство"

Проект реализует учет изделий производства без VBA:

- база данных: PostgreSQL;
- создание таблиц: `schema.sql`;
- начальные данные: `seed.sql`;
- добавление, изменение, удаление и поиск: SQL-запросы из Python;
- оконный интерфейс: Tkinter;
- поиск по индексируемым полям: `product_code`, `release_year`, `group_id`;
- отчет: вывод в таблицу и экспорт в `.csv` или `.txt`.

## Структура

```text
course_db/
├── schema.sql
├── seed.sql
├── app.py
├── requirements.txt
└── README.md
```

## Таблицы

`product_groups` - справочник групп изделий.

`products` - основная таблица изделий:

- `product_id` - первичный ключ;
- `product_code` - обозначение изделия;
- `group_id` - код группы изделия;
- `release_year` - год выпуска;
- `output_volume` - объем выпуска;
- `metal_consumption` - расход металла;
- `note` - примечание.

## Индексы

В `schema.sql` созданы индексы:

```sql
CREATE INDEX idx_products_code ON products(product_code);
CREATE INDEX idx_products_year ON products(release_year);
CREATE INDEX idx_products_group_id ON products(group_id);
```

Поиск в приложении выполняется по точному коду изделия, году выпуска или выбранной группе. Эти условия позволяют PostgreSQL использовать созданные индексы.

## Подготовка базы данных

Создайте базу данных:

```bash
createdb production_db
```

Загрузите структуру и тестовые данные:

```bash
psql -d production_db -f schema.sql
psql -d production_db -f seed.sql
```

На Windows с PostgreSQL на нестандартном порту, например `5433`, можно выполнить:

```cmd
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -h localhost -p 5433 -U postgres -d production_db -f schema.sql
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -h localhost -p 5433 -U postgres -d production_db -f seed.sql
```

В начале SQL-файлов задано `SET client_encoding = 'UTF8';`, чтобы русские строки корректно загружались из файлов в кодировке UTF-8.

## Настройка подключения

По умолчанию приложение использует:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=production_db
DB_USER=postgres
DB_PASSWORD=postgres
```

Если параметры отличаются, задайте переменные окружения перед запуском.

Пример для PowerShell:

```powershell
$env:DB_NAME="production_db"
$env:DB_USER="postgres"
$env:DB_PASSWORD="your_password"
python app.py
```

## Установка и запуск

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Функции интерфейса

- `Добавить изделие` - вставляет запись в таблицу `products`;
- `Изменить изделие` - обновляет выбранную запись;
- `Удалить изделие` - удаляет выбранную запись;
- `Найти по коду или году` - ищет запись по индексируемым полям;
- `Найти по группе` - ищет изделия по коду группы;
- `Сформировать отчет` - сохраняет текущие строки таблицы в файл `.csv` или `.txt`.
