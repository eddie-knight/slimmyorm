
import mysql.connector

from .mysql_connection import ORM


CURSOR = ORM.cursor(buffered=True, dictionary=True)


def dict_to_table_insert(table, data, truncate=True):
    results = []
    if truncate:
        # In case data persisted, rebuild by default
        CURSOR.execute(f"TRUNCATE TABLE {table}")
        ORM.commit()
    for row in data:
        result = insert_row(table, row)
        results.append(result)
    ORM.commit()
    return results


def insert_row(table, row):
    keys = [
        item.lower()
        for item in row
    ]
    values = ()
    for item in row:
        data = row[item] if row[item] != "" else None
        values = values + (data,)
    statement = f"INSERT INTO {table} ({','.join(keys)}) VALUES ("
    first = True
    for value in values:
        if first:
            statement = f"{statement}%s"
            first = False
        else:
            statement = f"{statement}, %s"
    statement = f"{statement})"
    try:
        response = CURSOR.execute(statement, values)
    except mysql.connector.ProgrammingError as e:
        response = f"Error: {e}"
    return response
