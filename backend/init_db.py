"""
Database initialization script.
Run this script to create all database tables.

Usage:
    python init_db.py
"""

from app.core.database import Base, engine
from app.models import user, organization, document, presentation

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()
