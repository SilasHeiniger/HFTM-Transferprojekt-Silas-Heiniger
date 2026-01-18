"""Database setup script - creates tables and test user"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://passwordmanager:passwordmanager@localhost:5432/passwordmanager')

print("Connecting to database...")
engine = create_engine(DATABASE_URL)

# SQL to create tables and test user
setup_sql = """
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: users
CREATE TABLE IF NOT EXISTS users (
    user_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Table: folders
CREATE TABLE IF NOT EXISTS folders (
    folder_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Table: password_entries
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
);

-- Insert test user
INSERT INTO users (user_id, username, password_hash)
VALUES ('00000000-0000-0000-0000-000000000001', 'testuser', 'test_password_hash')
ON CONFLICT (user_id) DO NOTHING;
"""

try:
    with engine.connect() as conn:
        # Execute each statement separately
        for statement in setup_sql.split(';'):
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                conn.execute(text(statement))
        conn.commit()
    
    print("✓ Database tables created successfully!")
    print("✓ Test user created successfully!")
    print("\nDatabase is ready!")
    
except Exception as e:
    print(f"✗ Error setting up database: {e}")
    exit(1)