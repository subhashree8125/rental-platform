#!/usr/bin/env python3
"""
Migration script to add profile_image column to users table
"""
import pymysql
from urllib.parse import urlparse, unquote

def migrate():
    try:
        # Parse database URI
        db_uri = "mysql+pymysql://root:Hari%405502@localhost:3306/broklink"
        # Remove the mysql+pymysql:// prefix
        uri = db_uri.replace("mysql+pymysql://", "")
        
        # Parse user:password@host:port/database
        auth_and_host = uri.split("@")
        user_pass = auth_and_host[0].split(":")
        host_port_db = auth_and_host[1].split("/")
        host_port = host_port_db[0].split(":")
        
        db_user = user_pass[0]
        db_password = unquote(user_pass[1])  # URL decode the password
        db_host = host_port[0]
        db_port = int(host_port[1]) if len(host_port) > 1 else 3306
        db_name = host_port_db[1]
        
        # Connect to database
        connection = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Check if column already exists
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = 'users' 
                AND COLUMN_NAME = 'profile_image'
            """, (db_name,))
            
            result = cursor.fetchone()
            
            if result['count'] == 0:
                print("Adding profile_image column to users table...")
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN profile_image VARCHAR(200) NULL DEFAULT NULL 
                    AFTER mobile_number
                """)
                connection.commit()
                print("✅ Successfully added profile_image column")
            else:
                print("ℹ️  profile_image column already exists, skipping")
        
        connection.close()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        raise

if __name__ == "__main__":
    migrate()
