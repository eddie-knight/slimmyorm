import os

import mysql.connector

DB_NAME = os.getenv('MYSQL_DATABASE')
ORM = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST'),
    port=os.getenv('MYSQL_PORT', "3306"),
    user=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    database=DB_NAME)


class MysqlConnection():
    def run_statement(self, statement, multi=False):
        cursor = ORM.cursor(buffered=True, dictionary=True)
        cursor.execute(f"USE {DB_NAME}")
        cursor.execute(statement, multi=multi)
        return cursor

    def insert(self, statement, multi=False):
        try:
            cursor = self.run_statement(statement, multi)
        except mysql.connector.ProgrammingError as e:
            return f"Error: {e}"
        cursor.close()
        ORM.commit()
        return True

    def update(self, statement, multi=False):
        return self.insert(statement, multi)

    def fetch_one(self, statement):
        try:
            cursor = self.run_statement(statement)
            response = cursor.fetchone()
            cursor.close()
            return response
        except mysql.connector.ProgrammingError as e:
            return f"Error: {e}"

    def fetch_all(self, statement, multi=False):
        try:
            cursor = self.run_statement(statement, multi)
            response = cursor.fetchall()
            cursor.close()
            return response
        except BaseException as e:
            return f"Error: {e}"
