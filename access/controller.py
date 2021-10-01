import sqlite3 as sql
from sqlite3.dbapi2 import Cursor
from model.RowOrder import RowOrder
import os
from typing import Dict, List, Any, Tuple

PATH_DB = './backup/'
FILE_DB = 'pedidos.db'


def connection_db(function):
    def wrapper(*args, **kwars):
        conn = sql.connect(PATH_DB + FILE_DB)
        try:
            value = function(conn, *args, **kwars)
            print("Proceso completado Exitosamente")
        except sql.Error as e:
            print(f"Error en el proceso:\n\t{e}")
            value = None
        conn.commit()
        conn.close
        return value
    return wrapper


@connection_db
def create_db(conn: Cursor) -> None:
    pass


@connection_db
def create_table_orders(conn: Cursor) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE orders (
                'ID' INTEGER PRIMARY KEY,
                'FECHA' DATE,
                'MES' TEXT,
                'AÑO' INTEGER,
                'CLIENTE' TEXT,
                'PEDIDO #' TEXT,
                'REFERENCIA' TEXT,
                'COLOR' TEXT,
                'TALLAS' TEXT,
                'CANTIDAD' INTEGER,
                'PRECIO UND' REAL,
                'PRECIO TOTAL' REAL,
                'LINEA' TEXT,
                'MARCA' TEXT,
                'COLECCIÓN' TEXT,
                'VENDEDOR' TEXT,
                'COSTO' REAL,
                'COSTO TOTAL' REAL,
                'ESTADO' TEXT
                );
        """
    )


@connection_db
def insert_rows_orders(conn: Cursor, rowsOrder: List[Dict[str, Any]]) -> None:
    cursor = conn.cursor()
    list_rows = []
    sql_instruction = """INSERT INTO orders
                            ('ID', 'FECHA', 'MES', 'AÑO', 'CLIENTE', 'PEDIDO #', 'REFERENCIA', 'COLOR', 
                                'TALLAS', 'CANTIDAD', 'PRECIO UND', 'PRECIO TOTAL', 'LINEA', 'MARCA', 'COLECCIÓN', 
                                'VENDEDOR', 'COSTO', 'COSTO TOTAL', 'ESTADO')
                        VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
                        """

    for json_row in rowsOrder:
        list_rows.append((json_row['ID'], json_row['FECHA'], json_row['MES'], json_row['AÑO'], json_row['CLIENTE'], json_row['PEDIDO #'],
                         json_row['REFERENCIA'], json_row['COLOR'], json_row['TALLAS'], json_row['CANTIDAD'], json_row['PRECIO UND'],
                         json_row['PRECIO TOTAL'], json_row['LINEA'], json_row['MARCA'], json_row['COLECCIÓN'], json_row['VENDEDOR'],
                         json_row['COSTO'], json_row['COSTO TOTAL'], json_row['ESTADO']))

    cursor.executemany(sql_instruction, list_rows)


@connection_db
def delete_all(conn: Cursor):
    cursor = conn.cursor()
    sql_instruction = 'DELETE FROM orders;'
    cursor.execute(sql_instruction)


@connection_db
def delete_range(conn: Cursor, min_value: int, max_value: int):
    cursor = conn.cursor()
    to_delete = tuple(i for i in range(min_value, max_value + 1))
    sql_instruction = f'DELETE FROM orders WHERE ID IN {to_delete}'
    cursor.execute(sql_instruction)


@connection_db
def last_id_orders(conn: Cursor):
    cursor = conn.cursor()
    sql_instruction = 'SELECT max(id) from orders'
    cursor.execute(sql_instruction)
    value = cursor.fetchone()
    return value[0]


@connection_db
def last_number_order(conn: Cursor):
    cursor = conn.cursor()
    sql_instruction = 'SELECT "PEDIDO #" from orders WHERE ID = (SELECT MAX(ID) FROM orders)'
    cursor.execute(sql_instruction)
    value = cursor.fetchone()
    return value[0]


@connection_db
def read_all_orders(conn: Cursor, date: str) -> List[Tuple[Any]]:
    cursor = conn.cursor()
    sql_instruction = 'SELECT * from orders '
    if date:
        sql_instruction += f' WHERE FECHA >= "{date}"'
    sql_instruction += ' ORDER BY ID'
    cursor.execute(sql_instruction)
    value = cursor.fetchall()
    return value


def init_file() -> None:
    if not FILE_DB in os.listdir(PATH_DB):
        create_db()
        create_table_orders()
