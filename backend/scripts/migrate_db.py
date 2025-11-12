"""
Database migration script to add branding fields to organizations table
Run this after schema changes to update existing database
"""

import sys
import os

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from app.core.database import engine, get_db
from app.models.organization import Organization

def migrate_database():
    """Add missing branding columns to organizations table"""

    print("🔄 Migrating database schema...")

    with engine.connect() as conn:
        # Check if columns exist, if not add them
        columns_to_add = [
            ("logo_url", "VARCHAR"),
            ("primary_color", "VARCHAR(7) DEFAULT '#0078D4'"),
            ("secondary_color", "VARCHAR(7) DEFAULT '#106EBE'"),
            ("accent_color", "VARCHAR(7) DEFAULT '#00BCF2'"),
            ("font_family", "VARCHAR DEFAULT 'Arial'"),
            ("design_style", "VARCHAR DEFAULT 'professional'"),
        ]

        for column_name, column_type in columns_to_add:
            try:
                # Try to add the column
                sql = f"ALTER TABLE organizations ADD COLUMN {column_name} {column_type}"
                conn.execute(text(sql))
                conn.commit()
                print(f"  ✓ Added column: {column_name}")
            except Exception as e:
                if "duplicate column name" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"  - Column {column_name} already exists, skipping")
                else:
                    print(f"  ✗ Error adding {column_name}: {e}")

    print("✅ Migration complete!")
    print("\n📝 Next steps:")
    print("1. Restart the backend server")
    print("2. Log out and log back in to get a fresh token")

if __name__ == "__main__":
    migrate_database()
