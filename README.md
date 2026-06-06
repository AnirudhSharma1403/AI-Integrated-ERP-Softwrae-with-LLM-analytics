# AI-Powered HR ERP

A complete FastAPI + SQLite HR ERP with admin login, employee management, attendance, leave approvals, dashboard metrics, and lightweight AI-style recommendations.

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Default Login

- Username: `admin`
- Password: `admin123`

## Gemini AI Assistant

Place your Gemini API key in `.env`:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Then open `http://127.0.0.1:8000/ai-assistant`.

## Features

- Admin authentication with session login/logout
- Add, edit, delete, and list employees
- Mark and view attendance
- Apply, approve, and reject leave requests
- Dashboard totals for employees, present today, and employees on leave
- Gemini AI assistant with HR database context
- SQLite database with SQLAlchemy ORM
- Modular FastAPI project with templates and static files
