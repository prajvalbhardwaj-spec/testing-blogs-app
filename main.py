from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from app.database import engine, SessionLocal, Base
from app import models
from app.seed import run_seed
from app.routers import auth, users, blogs


# ── Lifespan: runs on startup ──────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create all tables
    Base.metadata.create_all(bind=engine)
    print("Tables created")

    # 2. Seed dummy data if tables are empty
    db = SessionLocal()
    try:
        run_seed(db)
    except Exception as e:
        print(f"Seed error: {e}")
        db.rollback()
    finally:
        db.close()

    yield  # App runs here


# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Blog API",
    description="A FastAPI blog application with JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Global error handler ───────────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )

# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(blogs.router)


# ── Root ───────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "API is running"}


# ── Manual seed endpoint ───────────────────────────────────────────────────────
@app.post("/seed", tags=["Health"])
def seed_endpoint():
    db = SessionLocal()
    try:
        seeded = run_seed(db)
        if seeded:
            return {"message": "Database seeded!"}
        return {"message": "Already seeded, skipping"}
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"detail": str(e)})
    finally:
        db.close()
