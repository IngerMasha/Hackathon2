import os

import psycopg2
from psycopg2 import sql
from typing import List, Tuple


def create_database(dbname: str, user: str, password: str, host: str, port: str):
    """Создание новой базы данных, если она не существует"""
    conn = None
    try:
        # Подключение к postgres (базе данных по умолчанию)
        conn = psycopg2.connect(
            # dbname=dbname,
            dbname="postgres",
            user=user,
            password=password,
            host=host,
            port=port
        )
        conn.autocommit = True  # Включение автоматической фиксации изменений
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"), [dbname])
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
                print(f"Database {dbname} created successfully.")
            else:
                print(f"Database {dbname} already exists.")
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_connection(dbname: str, user: str, password: str, host: str):
    """Создание подключения к базе данных PostgreSQL"""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        return conn
    except Exception as e:
        print(e)
    return conn


def table_exists(conn, table_name: str) -> bool:
    """Проверяет, существует ли таблица в базе данных"""
    check_table_sql = sql.SQL("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = %s
    );
    """)
    try:
        with conn.cursor() as cursor:
            cursor.execute(check_table_sql, (table_name,))
            exists = cursor.fetchone()[0]
            return exists
    except Exception as e:
        print(e)
        return False


def create_file(directory: str, filename: str):
    """Создание файла для записи данных"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    if not os.path.exists(file_path):
        with open(file_path, 'w',  encoding='utf-8') as file:
            file.write("id, category, address, latitude, longitude\n")
    return file_path

def insert_data_to_file(file_path: str, data: tuple):
    """Запись данных в файл"""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"{data[0]}, {data[1]}, {data[2]}, {data[3]}, {data[4]}\n")


def create_table(conn, bbox: Tuple[float, float, float, float], table_name: str):
    """Создание таблицы на основе координат bbox"""
    print(table_name)
    # table_name = f"bbox_{bbox[0]}_{bbox[1]}_{bbox[2]}_{bbox[3]}".replace('.', '_')
    if table_exists(conn, table_name):
        print(f"Table {table_name} already exists.")
        return
    create_table_sql = sql.SQL("""
    CREATE TABLE {} (
        id SERIAL PRIMARY KEY,
        object_id INTEGER,
        type TEXT NOT NULL,
        address TEXT,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION
    );
    """).format(sql.Identifier(table_name))
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_sql)
            conn.commit()
            print(f"Table {table_name} created successfully.")
    except Exception as e:
        print(e)

def delete_all_tables(conn):
    """Удаляет все таблицы в базе данных"""
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
            DO $$ DECLARE
            r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
            """)
            conn.commit()
            print("All tables deleted successfully.")
    except Exception as e:
        print(e)
def insert_data(conn, table_name: str, data: Tuple[int, str, str, float, float]):
    """Вставка данных в таблицу на основе координат bbox"""
    if not table_exists(conn, table_name):
        print(f"Table {table_name} does not exist. Please create the table first.")
        return
    insert_data_sql = sql.SQL("""
    INSERT INTO {} (object_id, type, address, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    """).format(sql.Identifier(table_name))
    try:
        with conn.cursor() as cursor:
            cursor.execute(insert_data_sql, data)
            conn.commit()
            print(f"Data inserted successfully into {table_name}.")
    except Exception as e:
        print(e)

# Пример использования
# bbox = (11.4816, 41.8781, 12.5018, 41.8897)
# data = [
#     (227543966, "fuel", "n/a n/a", 41.8794856, 12.5081043),
#     (246574145, "drinking_water", "n/a n/a", 41.8791, 12.4826)
# ]
#
# host = "localhost"
# database = "Hackathon2"
# user = "postgres"
# password = "0000000000"
# port = "5432"
# create_database(database, user, password, host, port)
#
# conn = create_connection(database,user,password,host)
# if conn:
#     create_table(conn, bbox)
#     insert_data(conn, bbox, data)
#     conn.close()
