import bcrypt
from app.database import SessionLocal
from app import models


def hash_pw(password: str) -> str:
    return bcrypt.hashpw(
        password.encode("utf-8")[:72],
        bcrypt.gensalt()
    ).decode("utf-8")


def run_seed(db):
    """
    Insert dummy data if tables are empty.
    Returns True if seeded, False if data already existed.
    """
    if db.query(models.User).count() > 0:
        print("Database already has data, skipping seed")
        return False

    # ── Users ────────────────────────────────────────────
    alice = models.User(
        username="alice",
        email="alice@example.com",
        hashed_password=hash_pw("password123"),
    )
    bob = models.User(
        username="bob",
        email="bob@example.com",
        hashed_password=hash_pw("password123"),
    )
    charlie = models.User(
        username="charlie",
        email="charlie@example.com",
        hashed_password=hash_pw("password123"),
    )
    db.add_all([alice, bob, charlie])
    db.flush()

    # ── Blogs ────────────────────────────────────────────
    blogs = [
        models.Blog(
            title="Welcome to My Blog",
            content="Hello everyone! This is my very first blog post. I'm excited to share my thoughts with the world.",
            owner_id=alice.id,
        ),
        models.Blog(
            title="Getting Started with FastAPI",
            content="FastAPI is a modern, fast web framework for building APIs with Python 3.9+. It's incredibly easy to use.",
            owner_id=alice.id,
        ),
        models.Blog(
            title="Why I Love PostgreSQL",
            content="PostgreSQL is one of the most powerful open-source relational databases available today. Here's why I use it for all my projects.",
            owner_id=bob.id,
        ),
        models.Blog(
            title="Top 5 Python Tips",
            content="After years of writing Python, here are my top 5 tips that every developer should know to write cleaner, faster code.",
            owner_id=bob.id,
        ),
        models.Blog(
            title="My Journey into Tech",
            content="It all started when I picked up my first programming book. Here's the story of how I became a software developer.",
            owner_id=charlie.id,
        ),
    ]
    db.add_all(blogs)
    db.commit()

    print("Database seeded with dummy data")
    return True
