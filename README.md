# goit-pythonweb-hw-06

## Installation and Launch

## Running in VS Code Windows

Open the project folder in VS Code.

To run the project, follow these steps:

1. Create .env and set your password:
   `POSTGRES_PASSWORD=My_Secret_Password`

- Docker Compose automatically loads environment variables such as ${POSTGRES_PASSWORD}.

2. Specify the database URL (replace values with your own):
   `DATABASE_URL="postgresql://<username>:<password>@<host>:<port>/<database>"`

## Docker — Running on Windows (PowerShell or CMD)

```bash
docker compose up --build
```

- This command will create the database with tables, populate them with fake data, and execute a database query.

## If you need to populate the tables with different data and run a new query

Open a new terminal window.

1. Open a new terminal window.

```bash
docker exec db-app-hw06 python seed.py
```

2. Execute the database query:

```bash
docker exec db-app-hw06 python my_select.py
```

## How can I view the tables in the DB terminal later?

1. Open a new terminal window and enter:

```bash
docker exec -it db-hw06 psql -U postgres
```

2. Then run any SQL commands you need, for example:

```sql
SELECT 'grades' AS table_name, COUNT(*) AS row_count FROM grades
UNION ALL
SELECT 'groups', COUNT(*) FROM groups
UNION ALL
SELECT 'students', COUNT(*) FROM students
UNION ALL
SELECT 'subjects', COUNT(*) FROM subjects
UNION ALL
SELECT 'teachers', COUNT(*) FROM teachers
ORDER BY row_count DESC;
```
