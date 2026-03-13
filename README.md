# Blog API

A production-ready FastAPI blog application with JWT authentication and PostgreSQL.

## Features

- User registration & login (JWT)
- Create, read, update, delete blog posts
- Auto-creates tables and seeds dummy data on first run
- Fully containerized with Docker
- Ready to deploy on Render

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/prajvalbhardwaj-spec/testing-blogs-app.git
cd testing-blogs-app
```

### 2. Create your `.env` file

```bash
cp .env.example .env
# Edit .env and set your DATABASE_URL and SECRET_KEY
```

### 3. Run the app (macOS/Linux)

```bash
./start.sh
```

### 3. Run the app (Windows)

```bat
start.bat
```

The script will:
- Install all dependencies
- Seed the database with dummy data
- Start the server at `http://localhost:8000`

---

## Manual Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Seed the database manually
python seed.py

# Start the server
python -m uvicorn main:app --reload
```

---

## API Endpoints

| Method | Endpoint          | Auth Required | Description          |
|--------|-------------------|---------------|----------------------|
| GET    | `/`               | No            | Health check         |
| POST   | `/seed`           | No            | Manually seed DB     |
| POST   | `/auth/register`  | No            | Register a user      |
| POST   | `/auth/login`     | No            | Login, get JWT token |
| GET    | `/users/`         | No            | List all users       |
| GET    | `/users/me`       | Yes           | Get current user     |
| GET    | `/users/{id}`     | No            | Get user by ID       |
| DELETE | `/users/{id}`     | Yes           | Delete own account   |
| POST   | `/blogs/`         | Yes           | Create a blog post   |
| GET    | `/blogs/`         | No            | List all blogs       |
| GET    | `/blogs/{id}`     | No            | Get blog by ID       |
| PUT    | `/blogs/{id}`     | Yes           | Update own blog      |
| DELETE | `/blogs/{id}`     | Yes           | Delete own blog      |

Interactive docs available at: `http://localhost:8000/docs`

---

## Deploy to Render

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and create a new **Web Service**
3. Connect your GitHub repository
4. Set environment variables:
   - `DATABASE_URL` — your PostgreSQL connection string
   - `SECRET_KEY` — a long random secret
5. Render will auto-detect `render.yaml` and configure the service

---

## Docker

```bash
# Build image
docker build -t blog-api .

# Run container
docker run -p 10000:10000 --env-file .env blog-api
```
