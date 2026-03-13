# CLAUDE.md — Project Rules & Architecture Guidelines

These rules MUST be followed in every session, for every change, without exception.

---

## 1. Project Structure

Always create a modular structure:
- `app/` folder for all source code
- `.env` file for secrets (never commit this)
- `requirements.txt` for dependencies

---

## 2. Compatibility

- Target Python 3.9+
- **CRITICAL:** Do NOT use the `|` operator for type unions (e.g., `str | None`).
- Use `from typing import Optional` instead (e.g., `Optional[str]`).

---

## 3. Database

- Use SQLAlchemy (2.0 style) and Pydantic (v2)
- Use Alembic for database migrations
- **IMPORTANT:** On app startup, auto-create all tables AND auto-seed dummy data if tables are empty.
- The app must work out-of-the-box when connected to a brand new empty database.

---

## 4. Dependencies (`requirements.txt`)

- **NEVER** pin version numbers in `requirements.txt`
- Write ONLY the package name, one per line
- Example: `fastapi` NOT `fastapi==0.100.0`
- No `==`, `>=`, or `~=` version specifiers at all

---

## 5. Deployment-Ready

- Include a `Dockerfile` for containerized deployment
- Include a `render.yaml` for Render deployment
- Use environment variables for all secrets
- When creating a PostgreSQL database on Render, set Access Control to allow ALL inbound traffic (`0.0.0.0/0`) so it is accessible from anywhere.

---

## 6. GitHub Integration (CRITICAL)

- At the VERY START of any new project, before generating any code, ask ONLY for the GitHub repository URL.
- Do NOT ask anything else. No other questions.
- Initialize git and set the remote origin to that GitHub URL immediately.

---

## 7. Git Commits (MANDATORY)

- After EVERY change, new feature, or fix: automatically `git add`, `git commit` with a descriptive message, and `git push` to GitHub.
- **Never skip this step.**
- Commit messages should be clear, for example:
  - `feat: add database connection setup`
  - `fix: resolve seed script error`

---

## 8. Password Hashing (CRITICAL — Avoid bcrypt bugs)

- **Do NOT use `passlib`** for password hashing. It has compatibility issues with newer versions of bcrypt (`AttributeError on __about__`).
- Instead, use `bcrypt` directly:

```python
import bcrypt
hashed = bcrypt.hashpw(
    password.encode('utf-8')[:72],
    bcrypt.gensalt()
)
```

- **ALWAYS** truncate passwords to 72 bytes BEFORE hashing: `password.encode('utf-8')[:72]`
- Add `bcrypt` to `requirements.txt` (NOT `passlib`)

---

## 9. Startup Scripts (CRITICAL)

- Create a `start.sh` script (macOS/Linux) that:
  1. Installs dependencies: `pip install -r requirements.txt`
  2. Runs `python seed.py` to seed the database
  3. Starts the server: `uvicorn main:app --reload`

- Create a `start.bat` script (Windows) that:
  1. Installs dependencies: `pip install -r requirements.txt`
  2. Runs `python seed.py` to seed the database
  3. Starts the server: `uvicorn main:app --reload`

- The scripts must run `seed.py` FIRST, then start the server. This is the correct order.
- Make `start.sh` executable: `chmod +x start.sh`
- Users should ONLY need to run `./start.sh` or `start.bat` to get the full app running.

---

## Summary Checklist (before every push)

- [ ] Code is in `app/` folder
- [ ] No version pins in `requirements.txt`
- [ ] No `str | None` syntax — use `Optional[str]`
- [ ] Password hashing uses `bcrypt` directly (not `passlib`)
- [ ] Auto-creates tables and seeds data on startup
- [ ] `Dockerfile` and `render.yaml` present
- [ ] `start.sh` and `start.bat` present and correct
- [ ] Changes committed and pushed to GitHub
