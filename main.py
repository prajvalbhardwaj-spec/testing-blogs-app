from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

from app.database import engine, SessionLocal, Base
from app import models
from app.auth import hash_password
from app.routers import auth, users, blogs

# ── Create all tables ──────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)


# ── Seed dummy data ────────────────────────────────────────────────────────────
def seed_data():
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            user1 = models.User(
                username="alice",
                email="alice@example.com",
                hashed_password=hash_password("password123"),
            )
            user2 = models.User(
                username="bob",
                email="bob@example.com",
                hashed_password=hash_password("password123"),
            )
            db.add_all([user1, user2])
            db.flush()

            blog1 = models.Blog(
                title="Welcome to the Blog",
                content="This is Alice's first blog post. Hello world!",
                owner_id=user1.id,
            )
            blog2 = models.Blog(
                title="Getting Started with FastAPI",
                content="FastAPI is a modern, fast web framework for building APIs with Python.",
                owner_id=user1.id,
            )
            blog3 = models.Blog(
                title="Bob's Thoughts",
                content="Here are some of Bob's thoughts on technology and life.",
                owner_id=user2.id,
            )
            db.add_all([blog1, blog2, blog3])
            db.commit()
            print("✅ Dummy data seeded successfully.")
        else:
            print("ℹ️  Data already exists, skipping seed.")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed error: {e}")
    finally:
        db.close()


seed_data()

# ── App ────────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Blog API",
    description="A FastAPI blog application with JWT authentication",
    version="1.0.0",
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
