import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

_pool = None

def get_connection():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="subtrack_pool",
            pool_size=5,
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "subtrack"),
        )
    return _pool.get_connection()

def query(sql, params=(), fetchone=False, commit=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params)
        result = cursor.fetchone() if fetchone else cursor.fetchall()
        if commit:
            conn.commit()
        return result
    finally:
        cursor.close()
        conn.close()

def execute(sql, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()
