"""Database setup script - creates tables and test user"""
import os
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://passwordmanager:passwordmanager@localhost:5432/passwordmanager')

print("Connecting to database...")
print(f"Database URL: {DATABASE_URL}")

# Wait for database to be ready
time.sleep(2)

try:
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✓ Database connection successful!")
        
except Exception as e:
    print(f"✗ Cannot connect to database: {e}")
    print("\nMake sure Docker container is running:")
    print("  docker ps")
    exit(1)

print("\nCreating database tables...")

try:
    with engine.connect() as conn:
        # Enable UUID extension
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
        conn.commit()
        
        # Create users table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                user_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            )
        """))
        conn.commit()
        print("✓ Created users table")
        
        # Create folders table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS folders (
                folder_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id UUID NOT NULL,
                name VARCHAR(100) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """))
        conn.commit()
        print("✓ Created folders table")
        
        # Create password_entries table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS password_entries (
                entry_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
                user_id UUID NOT NULL,
                folder_id UUID,
                name VARCHAR(100) NOT NULL,
                username VARCHAR(100),
                password TEXT,
                website_url VARCHAR(500),
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (folder_id) REFERENCES folders(folder_id) ON DELETE SET NULL
            )
        """))
        conn.commit()
        print("✓ Created password_entries table")
        
        # Insert test user
        conn.execute(text("""
            INSERT INTO users (user_id, username, password_hash)
            VALUES ('00000000-0000-0000-0000-000000000001', 'testuser', 'test_password_hash')
            ON CONFLICT (user_id) DO NOTHING
        """))
        conn.commit()
        print("✓ Created test user")
    
    print("\n✓✓✓ Database is ready! ✓✓✓")
    
except Exception as e:
    print(f"\n✗ Error setting up database: {e}")
    import traceback
    traceback.print_exc()
    exit(1)