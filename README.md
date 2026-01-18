# Password Manager

Simple password manager with search and password generation built with FastAPI.

## Requirements

- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
- **uv** - Install with: `pip install uv`

## Installation (Windows)

1. **Start Docker Desktop**

2. **Run the installer:**
   ```cmd
   install.bat
   ```

3. **Start the application:**
   ```cmd
   start.bat
   ```

4. **Open in browser:** http://localhost:8000

## What the installer does:

1. Starts PostgreSQL database in Docker
2. Installs Python dependencies
3. Creates `.env` configuration file
4. Sets up database tables and test user

## Manual Installation

```cmd
docker-compose -f docker-compose.db.yaml up -d
uv sync
copy .env.example .env
timeout /t 10 /nobreak >nul
uv run python setup_db.py
uv run python -m app.main
```

## Database

- **Host:** localhost:5432
- **User:** passwordmanager
- **Password:** passwordmanager
- **Database:** passwordmanager

## Stopping

- **Application:** Press `Ctrl+C`
- **Database:** `docker-compose -f docker-compose.db.yaml down`

## Security Warning

**This is a development/learning project. Do NOT use for real passwords without:**
- Implementing password encryption
- Adding proper user authentication
- Using HTTPS
- Changing default credentials