# Run This Project on Windows

Use these steps after reopening or restarting your computer.

## 1. Open PowerShell

Open PowerShell, then go to the project folder:

```powershell
cd "C:\Users\hp\Documents\New project"
```

## 2. Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once in the same PowerShell window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Start the FastAPI Server

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 4. Open the App

Open this URL in your browser:

```text
http://127.0.0.1:8000
```

## Login

```text
Username: admin
Password: admin123
```

## AI Assistant

The Gemini API key is stored in:

```text
C:\Users\hp\Documents\New project\.env
```

AI Assistant page:

```text
http://127.0.0.1:8000/ai-assistant
```

## Stop the Server

Press `Ctrl+C` in the PowerShell window where Uvicorn is running.
