from flask import jsonify
from sqlalchemy.dialects.postgresql import psycopg2
import psycopg2

import db
from db import get_connection, release_connection


def create_user_table():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""create table users(first_name varchar,
        last_name varchar,
        password varchar)""")
        conn.commit()
        cur.close()
        return True
    except psycopg2.Error as e:
        print(e)
        return False
    finally:
        release_connection(conn)
