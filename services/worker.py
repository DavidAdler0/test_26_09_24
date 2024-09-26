import psycopg2

from db import get_connection, release_connection


def insert_worker(data):
    conn = get_connection()
    try:
        cur = conn.cursor()

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        query = '''insert into workers(first_name, last_name, password) values(%s, %s, %s)'''
        params = (first_name, last_name, password)

        cur.execute(query, params)
        conn.commit()
        cur.close()
        return True
    except psycopg2.Error as e:
        print(e)
        return False
    finally:
        release_connection(conn)
def find_worker(find_by= None, value=None):
    conn = get_connection()
    try:
        cur = conn.cursor()
        encoded_find_by = find_by.split(' ')[0].strip()
        query = 'select * from workers'
        if find_by and value:
            query += f' where {encoded_find_by} = %s'
            params = (value,)
            cur.execute(query, params)
        else:
            cur.execute(query)
        users = cur.fetchall()
        return users
    except psycopg2.Error as e:
        print(e)
        return False
    finally:
        if cur:
            cur.close()
        release_connection(conn)


