"""
Standalone seed script.
Run manually: python seed.py
"""
from dotenv import load_dotenv
load_dotenv()

from app.database import engine, SessionLocal, Base
from app import models
from app.seed import run_seed

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created")

    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

    print("Database seeded successfully!")
