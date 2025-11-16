"""
Reset database script - drops all tables and recreates them.
Use this when you change the database schema during development.

WARNING: This will delete ALL data in the database!

Usage:
    python reset_db.py
"""

import os
from app.core.database import Base, engine

def reset_database():
    """Drop all tables and recreate them"""
    print("⚠️  WARNING: This will delete ALL data in the database!")

    # Drop all tables
    print("🗑️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped")

    # Recreate all tables
    print("📦 Creating tables with new schema...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    print("\n🎉 Database reset complete! You can now start the server.")

if __name__ == "__main__":
    reset_database()
