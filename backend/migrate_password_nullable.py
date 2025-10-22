"""
Migration script to make password_hash column nullable for Firebase Phone Auth users
"""
import pymysql
import urllib.parse

def migrate():
    connection = None
    try:
        # Parse the connection string from Config
        # mysql+pymysql://root:Hari%405502@localhost:3306/broklink
        connection_string = "mysql+pymysql://root:Hari%405502@localhost:3306/broklink"
        
        # Extract connection details
        # Format: mysql+pymysql://user:password@host:port/database
        parts = connection_string.replace("mysql+pymysql://", "").split("@")
        user_pass = parts[0].split(":")
        host_db = parts[1].split("/")
        host_port = host_db[0].split(":")
        
        user = user_pass[0]
        password = urllib.parse.unquote(user_pass[1])  # Decode URL-encoded password
        host = host_port[0]
        port = int(host_port[1])
        database = host_db[1]
        
        # Connect to database
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            print("🔄 Making password_hash column nullable...")
            
            # Alter the column to allow NULL values
            alter_query = """
                ALTER TABLE users 
                MODIFY COLUMN password_hash VARCHAR(200) NULL
            """
            cursor.execute(alter_query)
            connection.commit()
            
            print("✅ Migration completed successfully!")
            print("   - password_hash column is now nullable")
            print("   - Phone authentication users can now be created without passwords")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Firebase Phone Auth - Database Migration")
    print("Making password_hash nullable for phone-only users")
    print("=" * 60)
    migrate()
