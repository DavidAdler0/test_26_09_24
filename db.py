import psycopg2
from psycopg2 import pool


conn_pool = psycopg2.pool.SimpleConnectionPool(
    min= 1,
    max= 5,
    dbname="wwii_missions",
    user="postgres",
    password="da7104",
    host="localhost",
    port="5432"
)

def get_connection():
    if conn_pool:
        conn = conn_pool.getconn()
        return conn
def release_connection(conn):
    conn_pool.putconn(conn)
