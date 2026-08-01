# Mindsight-AI

The project is about mental health analysis.

## Local development

1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run migrations and start the development server:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

3. Visit http://127.0.0.1:8000/

Settings default to SQLite for local development.
