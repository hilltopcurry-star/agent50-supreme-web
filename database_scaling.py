# database_scaling.py
import psycopg2
from psycopg2 import pool
import os
from contextlib import contextmanager
import logging

class DatabaseScaler:
    def __init__(self):
        self.connection_pool = None
        self.setup_connection_pool()
    
    def setup_connection_pool(self):
        """Setup connection pool for better performance"""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=20,
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'king_deepseek'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', ''),
                port=os.getenv('DB_PORT', '5432')
            )
            print("✅ Database connection pool created")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
    
    @contextmanager
    def get_connection(self):
        """Get connection from pool with context manager"""
        connection = None
        try:
            connection = self.connection_pool.getconn()
            yield connection
        except Exception as e:
            logging.error(f"Database error: {e}")
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                self.connection_pool.putconn(connection)
    
    def create_tables(self):
        """Create optimized tables for scaling"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Users table with indexing
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        role VARCHAR(20) DEFAULT 'user',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_login TIMESTAMP,
                        is_active BOOLEAN DEFAULT TRUE
                    )
                ''')
                
                # Files table with partitioning
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS files (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        original_name VARCHAR(255) NOT NULL,
                        stored_name VARCHAR(255) NOT NULL,
                        file_size BIGINT NOT NULL,
                        file_type VARCHAR(50),
                        user_id INTEGER REFERENCES users(id),
                        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_public BOOLEAN DEFAULT FALSE
                    )
                ''')
                
                # Messages table for chat
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id),
                        message TEXT NOT NULL,
                        room VARCHAR(100) DEFAULT 'general',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Create indexes for performance
                cur.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
                cur.execute('CREATE INDEX IF NOT EXISTS idx_files_user_id ON files(user_id)')
                cur.execute('CREATE INDEX IF NOT EXISTS idx_files_upload_time ON files(upload_time)')
                cur.execute('CREATE INDEX IF NOT EXISTS idx_messages_room ON messages(room)')
                cur.execute('CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at)')
                
                conn.commit()
                print("✅ Database tables and indexes created")
    
    def get_database_stats(self):
        """Get database performance statistics"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT 
                        schemaname,
                        tablename,
                        attname,
                    n_distinct,
                    most_common_vals
                    FROM pg_stats
                    WHERE schemaname = 'public'
                    LIMIT 10
                ''')
                return cur.fetchall()