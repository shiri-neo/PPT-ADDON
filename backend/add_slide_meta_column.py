"""
Add meta column to slides table.
This script adds the missing 'meta' column without deleting existing data.

Usage:
    python add_slide_meta_column.py
"""

import sqlite3

def add_meta_column():
    """Add meta column to slides table if it doesn't exist"""
    # Connect to database
    conn = sqlite3.connect('pptai.db')
    cursor = conn.cursor()

    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(slides)")
        columns = [col[1] for col in cursor.fetchall()]

        if 'meta' in columns:
            print("✅ Column 'meta' already exists in slides table")
        else:
            print("📝 Adding 'meta' column to slides table...")
            cursor.execute("ALTER TABLE slides ADD COLUMN meta TEXT")
            conn.commit()
            print("✅ Successfully added 'meta' column to slides table")

        conn.close()
        print("\n🎉 Database schema updated successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        conn.close()
        raise

if __name__ == "__main__":
    add_meta_column()
