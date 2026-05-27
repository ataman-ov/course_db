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
***

# Ответы на вопросы

## 1. На какие части можно разделить язык SQL, какие команды им соответствуют?

Язык SQL делится на несколько основных частей:

| Часть SQL | Назначение | Основные команды |
|---|---|---|
| DDL (Data Definition Language) | Определение структуры базы данных | CREATE, ALTER, DROP |
| DML (Data Manipulation Language) | Работа с данными | INSERT, UPDATE, DELETE |
| DQL (Data Query Language) | Выполнение запросов | SELECT |
| DCL (Data Control Language) | Управление правами доступа | GRANT, REVOKE |
| TCL (Transaction Control Language) | Управление транзакциями | COMMIT, ROLLBACK, SAVEPOINT |

---

## 2. Для чего используются индексы?

Индексы используются для ускорения поиска и выборки данных в таблицах базы данных.

Основные преимущества индексов:

- ускорение выполнения запросов;
- уменьшение времени поиска данных;
- повышение производительности базы данных.

### Пример создания индекса

```sql
CREATE INDEX idx_product_code
ON products(product_code);
```

---

## 3. Как обновить несколько полей для нескольких кортежей таблицы одним запросом?

Для обновления нескольких полей используется команда `UPDATE`.

### Пример

```sql
UPDATE products
SET
    output_volume = 2000,
    metal_consumption = 450.75
WHERE release_year = 2023;
```

Данный запрос изменяет сразу несколько полей для всех строк, удовлетворяющих условию.

---

## 4. Что определяет ключевое слово CONSTRAINT?

Ключевое слово `CONSTRAINT` используется для задания ограничений целостности данных.

С помощью `CONSTRAINT` определяются:

- PRIMARY KEY;
- FOREIGN KEY;
- UNIQUE;
- CHECK;
- NOT NULL.

### Пример

```sql
CONSTRAINT fk_products_group
FOREIGN KEY (group_id)
REFERENCES product_groups(group_id)
```

---

## 5. Что такое VBA?

VBA (Visual Basic for Applications) — язык программирования, встроенный в продукты Microsoft Office.

VBA используется для:

- автоматизации работы;
- создания форм;
- обработки данных;
- написания макросов;
- управления базами данных MS Access.

---

## 6. Можно ли выполнить добавление данных без указания названия полей, в которые добавляются значения?

Да, можно, если значения указываются в том же порядке, в котором поля созданы в таблице.

### Пример без указания полей

```sql
INSERT INTO product_groups
VALUES (1, 'Детали');
```

Однако такой способ не рекомендуется, потому что:

- можно ошибиться в порядке полей;
- запрос станет неработоспособным после изменения структуры таблицы;
- ухудшается читаемость кода.

### Рекомендуемый вариант

```sql
INSERT INTO product_groups (group_id, group_name)
VALUES (1, 'Детали');
```

