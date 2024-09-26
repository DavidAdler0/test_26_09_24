from postgres_proj.db import get_db_connection
import psycopg2

from db import release_connection


def normalize_db():
    t_conn = get_db_connection()
    s_conn = get_db_connection()


    try :
        query1 = """
            CREATE TABLE contrys(
                    country_id SERIAL PRIMARY KEY,
                    country_name distinct VARCHAR(100)
            )
        """
        query2 = """
            CREATE TABLE citys(
                    city_id SERIAL PRIMARY KEY,
                    country_id int references countrys(country_id),
                    city_name VARCHAR(100)
                    add constraint distinct_citys unique (country_id, city_name)
            )
        """
        query3 = """
            CREATE TABLE locations(
                    location_id SERIAL PRIMARY KEY,
                    city_id int references citys(city_id),
                    location_latitude NUMERIC(10, 6),
                    location_longitude NUMERIC(10, 6)
                    add constraint distinct_locations unique (city_id, location_latitude, location_longitude)
            )
        """
        query4 = """
            CREATE TABLE targets (
                target_id SERIAL PRIMARY KEY,
                location_id INT REFERENCES locations(location_id),
                target_type VARCHAR(100),
                target_industry VARCHAR(255),
                target_priority VARCHAR(5),
            )
        """

        # execute the queries
        t_cur = t_conn.cursor()
        t_cur.executemany([query1, query2, query3, query4])
        t_conn.commit()

        s_cur = s_conn.cursor()
        s_cur.execute("SELECT * FROM mission")
        while True:
            mission_row = s_cur.fetchone()
            if mission_row is None:
                break

            country = mission_row[14]
            city = mission_row[15]
            latitude = mission_row[19]
            longitude = mission_row[20]
            target_type = mission_row[16]
            target_industry = mission_row[17]
            target_priority = mission_row[18]
            try:

                t_cur.execute("INSERT INTO contrys (country_name)"
                            " VALUES (%s,) RETURNING country_id",
                            (country,))

                country_id = t_cur.fetchone()[0]
            except psycopg2.errors.UniqueViolation:
                pass

            try:
                t_cur.execute("INSERT INTO citys (country_id, city_name)"
                              " VALUES (%s,%s) RETURNING city_id",
                              (country_id, city))

                city_id = t_cur.fetchone()[0]
            except psycopg2.errors.UniqueViolation:
                pass

            try:
                t_cur.execute("INSERT INTO locations (city_id, location_latitude, location_longitude)"
                              " VALUES (%s,%s,%s) RETURNING location_id",
                              (city_id, latitude, longitude))

                location_id = t_cur.fetchone()[0]
            except psycopg2.errors.UniqueViolation:
                pass

            t_cur.execute("INSERT INTO targets (location_id, target_type, target_industry, target_priority)"
                          " VALUES (%s,%s,%s,%s) RETURNING target_id",
                          (location_id, target_type, target_industry, target_priority))

            target_id = t_cur.fetchone()[0]
            mission_row[13] = target_id

            t_conn.commit()
            s_conn.commit()



    except psycopg2.Error:
        t_conn.rollback()
    finally:
        if t_cur:
            t_cur.close()
        if s_cur:
            s_cur.close()
        release_connection(t_conn)
        release_connection(s_conn)

def change_mission_table_query():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
                alter table mission
                drop column target_id,
                drop column target_country,
                drop column target_city,
                drop column target_type,
                drop column target_industry,
                drop column target_priority,
                drop column target_latitude,
                drop column target_longitude
            """
        cur.execute(query)
        conn.commit()
    except psycopg2.Error:
        conn.rollback()
    finally:
        if cur:
            cur.close()
        conn.close()
