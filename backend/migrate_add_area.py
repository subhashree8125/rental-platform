"""
Migration script to add 'area' column to properties table
Run this once to update your database schema
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import create_app
from backend.db import db
from sqlalchemy import text

def migrate_add_area_column():
    """Add area column to properties table and set default values"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name='properties' 
                AND column_name='area'
            """))
            
            column_exists = result.scalar() > 0
            
            if column_exists:
                print("✅ Column 'area' already exists in properties table")
            else:
                # Add the area column after city
                print("📝 Adding 'area' column to properties table...")
                db.session.execute(text("""
                    ALTER TABLE properties 
                    ADD COLUMN area VARCHAR(100) 
                    AFTER city
                """))
                db.session.commit()
                print("✅ Column 'area' added successfully")
            
            # Update existing properties with default area value
            print("📝 Updating existing properties with default area values...")
            db.session.execute(text("""
                UPDATE properties 
                SET area = 'Area Not Specified' 
                WHERE area IS NULL OR area = ''
            """))
            db.session.commit()
            print("✅ Existing properties updated with default area values")
            
            # Make the column NOT NULL
            if not column_exists:
                print("📝 Making 'area' column NOT NULL...")
                db.session.execute(text("""
                    ALTER TABLE properties 
                    MODIFY COLUMN area VARCHAR(100) NOT NULL
                """))
                db.session.commit()
                print("✅ Column 'area' set to NOT NULL")
            
            # Show statistics
            result = db.session.execute(text("SELECT COUNT(*) FROM properties"))
            total_properties = result.scalar()
            print(f"\n📊 Migration complete!")
            print(f"   Total properties in database: {total_properties}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during migration: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Starting migration to add 'area' column...")
    print("=" * 60)
    migrate_add_area_column()
    print("=" * 60)
    print("✨ Migration process completed!")
