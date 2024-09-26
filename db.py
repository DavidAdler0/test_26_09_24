import psycopg2
from psycopg2 import pool
from flask_sqlalchemy import SQLAlchemy


conn_pool = psycopg2.pool.SimpleConnectionPool(
    minconn= 1,
    maxconn= 5,
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


db = SQLAlchemy()