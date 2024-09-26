from db import get_connection, release_connection
import psycopg2




def normalize_db():
    try:
        t_conn = get_connection()
        s_conn = get_connection()
        t_cur = t_conn.cursor()
        s_cur = s_conn.cursor()
    except psycopg2.Error as e:
        print(e)


    try :
        query1 = """
            CREATE TABLE contreis(
                    country_id SERIAL PRIMARY KEY,
                    country_name VARCHAR(100),
                    unique(country_name)
            )
        """
        query2 = """
            CREATE TABLE citys(
                    city_id SERIAL PRIMARY KEY,
                    country_id int references contreis(country_id),
                    city_name VARCHAR(100),
                    unique (country_id, city_name)
            )
        """
        query3 = """
            CREATE TABLE locations(
                    location_id SERIAL PRIMARY KEY,
                    city_id int references citys(city_id),
                    location_latitude NUMERIC(10, 6),
                    location_longitude NUMERIC(10, 6),
                    unique (city_id, location_latitude, location_longitude)
            )
        """
        query4 = """
            CREATE TABLE targets (
                target_id SERIAL PRIMARY KEY,
                location_id INT REFERENCES locations(location_id),
                target_type VARCHAR(100),
                target_industry VARCHAR(255),
                target_priority VARCHAR(5)
            )
        """
        query5 = '''
        CREATE TABLE fixed_mission(
            mission_id INTEGER PRIMARY KEY,                 -- Mission ID, auto-incremented primary key
            mission_date DATE,                             -- Mission Date, a date field
            theater_of_operations VARCHAR(100),            -- Theater of Operations, assuming text data
            country VARCHAR(100),                          -- Country, assuming text data
            air_force VARCHAR(100),                        -- Air Force, assuming text data
            unit_id VARCHAR(100),                          -- Unit ID, assuming text data
            aircraft_series VARCHAR(100),                  -- Aircraft Series, assuming text data
            callsign VARCHAR(100),                         -- Callsign, assuming text data
            mission_type VARCHAR(100),                     -- Mission Type, assuming text data
            takeoff_base VARCHAR(255),                     -- Takeoff Base, assuming larger text data
            takeoff_location VARCHAR(255),                 -- Takeoff Location, assuming larger text data
            takeoff_latitude VARCHAR(15),               -- Takeoff Latitude, assuming GPS latitude
            takeoff_longitude NUMERIC(10, 6),              -- Takeoff Longitude, assuming GPS longitude
            target_id VARCHAR(100),                        -- Target ID, assuming text or unique identifier
            target_country VARCHAR(100),                   -- Target Country, assuming text data
            target_city VARCHAR(100),                      -- Target City, assuming text data
            target_type VARCHAR(100),                      -- Target Type, assuming text data
            target_industry VARCHAR(255),                  -- Target Industry, assuming text data
            target_priority VARCHAR(5),                       -- Target Priority, assuming numerical data
            target_latitude NUMERIC(10, 6),                -- Target Latitude, assuming GPS latitude
            target_longitude NUMERIC(10, 6),               -- Target Longitude, assuming GPS longitude
            altitude_hundreds_of_feet NUMERIC(7, 2),             -- Altitude in hundreds of feet, assuming numerical data
            airborne_aircraft NUMERIC(4, 1),                     -- Airborne Aircraft, assuming numerical data
            attacking_aircraft INTEGER,                    -- Attacking Aircraft, assuming numerical data
            bombing_aircraft INTEGER,                      -- Bombing Aircraft, assuming numerical data
            aircraft_returned INTEGER,                     -- Aircraft Returned, assuming numerical data
            aircraft_failed INTEGER,                       -- Aircraft Failed, assuming numerical data
            aircraft_damaged INTEGER,                      -- Aircraft Damaged, assuming numerical data
            aircraft_lost INTEGER,                         -- Aircraft Lost, assuming numerical data
            high_explosives VARCHAR(255),                  -- High Explosives, assuming text
            high_explosives_type VARCHAR(255),             -- High Explosives Type, assuming text data
            high_explosives_weight_pounds VARCHAR(25),  -- High Explosives Weight in Pounds, assuming decimal data
            high_explosives_weight_tons NUMERIC(10, 2),    -- High Explosives Weight in Tons, assuming decimal data
            incendiary_devices VARCHAR(255),               -- Incendiary Devices, assuming text data
            incendiary_devices_type VARCHAR(255),          -- Incendiary Devices Type, assuming text data
            incendiary_devices_weight_pounds NUMERIC(10, 2), -- Incendiary Devices Weight in Pounds, assuming decimal data
            incendiary_devices_weight_tons NUMERIC(10, 2),   -- Incendiary Devices Weight in Tons, assuming decimal data
            fragmentation_devices VARCHAR(255),            -- Fragmentation Devices, assuming text data
            fragmentation_devices_type VARCHAR(255),       -- Fragmentation Devices Type, assuming text data
            fragmentation_devices_weight_pounds NUMERIC(10, 2), -- Fragmentation Devices Weight in Pounds, assuming decimal data
            fragmentation_devices_weight_tons NUMERIC(10, 2),   -- Fragmentation Devices Weight in Tons, assuming decimal data
            total_weight_pounds NUMERIC(10, 2),            -- Total Weight in Pounds, assuming decimal data
            total_weight_tons NUMERIC(10, 2),              -- Total Weight in Tons, assuming decimal data
            time_over_target VARCHAR(8),                         -- Time Over Target, assuming time data
            bomb_damage_assessment VARCHAR(255),           -- Bomb Damage Assessment, assuming text data
            source_id VARCHAR(100)                         -- Source ID, assuming text or unique identifier
        );
        '''

        # execute the queries
        queries = [query1, query2, query3, query4, query5]
        for query in queries:
            t_cur.execute(query)
        t_conn.commit()

        s_cur.execute("SELECT * FROM mission")
        while True:
            mission_row = s_cur.fetchone()
            if mission_row is None:
                break

            mission_id = mission_row[0]
            country = mission_row[14]
            city = mission_row[15]
            latitude = mission_row[19]
            longitude = mission_row[20]
            target_type = mission_row[16]
            target_industry = mission_row[17]
            target_priority = mission_row[18]
            try:

                params = (country,)
                query = "INSERT INTO contreis (country_name) VALUES (%s) RETURNING country_id"
                t_cur.execute(query, params)
                country_id = t_cur.fetchone()[0]
            except psycopg2.errors.UniqueViolation:
                pass

            try:
                query = "INSERT INTO citys (country_id, city_name) VALUES (%s,%s) RETURNING city_id"
                params = (country_id, city)
                t_cur.execute(query, params)


                city_id = t_cur.fetchone()[0]
            except psycopg2.errors.UniqueViolation:
                pass

            try:
                query = "INSERT INTO locations (city_id, location_latitude, location_longitude) VALUES (%s,%s,%s) RETURNING location_id"
                params = (city_id, latitude, longitude)
                t_cur.execute(query, params)

                location_id = t_cur.fetchone()[0]
            except psycopg2.errors.UniqueViolation:
                pass

            query = "INSERT INTO targets (location_id, target_type, target_industry, target_priority) VALUES (%s,%s,%s,%s) RETURNING target_id",
            params = (location_id, target_type, target_industry, target_priority)
            t_cur.execute(query, params)

            target_id = t_cur.fetchone()[0]

            t_cur.execute("insert into fixed_mission select * from mission", ())

            params = (target_id, mission_id)
            update_target_query = "update fixed_mission set target_id = %s where mission_id = %s"
            t_cur.execute(update_target_query, params)
            t_conn.commit()

    except psycopg2.Error as e:
        t_conn.rollback()
        print(e)
    finally:
        t_cur.close()
        s_cur.close()
        release_connection(t_conn)
        release_connection(s_conn)

normalize_db()

def change_mission_table_query():
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = """
                alter table mission
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
