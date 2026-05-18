import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "easyjob.db")

def add_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check existing columns
    cursor.execute("PRAGMA table_info(applications)")
    columns = [column[1] for column in cursor.fetchall()]
    
    print("Existing columns:", columns)
    
    # Add match_score if it doesn't exist
    if 'match_score' not in columns:
        cursor.execute("ALTER TABLE applications ADD COLUMN match_score REAL")
        print("✅ Added match_score column")
    else:
        print("⚠️ match_score column already exists")
    
    # Add parsed_skills if it doesn't exist
    if 'parsed_skills' not in columns:
        cursor.execute("ALTER TABLE applications ADD COLUMN parsed_skills TEXT")
        print("✅ Added parsed_skills column")
    else:
        print("⚠️ parsed_skills column already exists")
    
    conn.commit()
    conn.close()
    print("\n✅ Database updated successfully!")

if __name__ == "__main__":
    add_columns()