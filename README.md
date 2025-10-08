# Text Viewer Web App

A lightweight Flask application backed by SQLAlchemy that lets you upload, browse, edit, and delete `.txt` documents. The text lives directly in the database so everything stays searchable and easy to manage.

## Features

- Upload UTF-8 encoded TXT files and store both the display name and original filename.
- Read file content online with helpful metadata such as timestamps.
- Edit text inline or replace it by uploading a new TXT file.
- Delete documents you no longer need, with clear flash feedback for every action.
- Swap between MySQL, SQLite, or other SQLAlchemy-supported databases by changing the `DATABASE_URL`.

## Prerequisites

- Python 3.10 or newer
- MySQL 8.0+ (or a compatible MariaDB release) – optional if you stick with the default SQLite database
- A virtual environment is recommended to isolate dependencies

## Quick start

1. **Clone the repository and enter the folder**

   ```powershell
   git clone <your-repo-url>
   cd textviewer
   ```

2. **Create and activate a virtual environment**

   ```powershell
   py -3 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure the database connection**

   The application uses SQLite (`textviewer.db`) by default. To connect to your Azure PostgreSQL instance:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   Fill in the `POSTGRES_*` entries with your server credentials. They map to the values Azure displays in the connection string, for example:

   ```
   POSTGRES_USER=bsgwfnomek
   POSTGRES_PASSWORD=<your_password>
   POSTGRES_HOST=text-server.postgres.database.azure.com
   POSTGRES_PORT=5432
   POSTGRES_DB=postgres
   ```

   Alternatively, you can set a full SQLAlchemy URL via `DATABASE_URL`, e.g.:

   ```
   postgresql+psycopg2://bsgwfnomek:<your_password>@text-server.postgres.database.azure.com:5432/postgres?sslmode=require
   ```

5. **Run the development server**

   ```powershell
   flask --app run run
   ```

   Visit `http://127.0.0.1:5000/` (or the host configured in `run.py`) in your browser to try it out.

## Running tests

```powershell
pytest
```

The test suite uses an in-memory SQLite database, so it will not touch your real data.

## Project structure

```
textviewer/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   └── css/main.css
│   └── templates/
│       ├── base.html
│       ├── detail.html
│       ├── edit.html
│       └── index.html
├── tests/
│   ├── conftest.py
│   └── test_app.py
├── .env.example
├── README.md
├── requirements.txt
└── run.py
```

## Deployment tips

- Provide production-ready environment variables such as `SECRET_KEY` and `DATABASE_URL`, and disable debug mode.
- Run the app behind a WSGI server like Gunicorn or uWSGI, optionally fronted by Nginx.
- Consider adding Flask-Migrate if you expect schema changes in the future.

Have ideas to extend the project? Full-text search, pagination, authentication, or audit logging all fit nicely on top of this foundation.
