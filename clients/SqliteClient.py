import sqlite3 as sql

class SqlClient():

    def __init__(self, db_path):
        self.conn = sql.connect(db_path if db_path else './kaggle/input/basketball/basketball.sqlite')


    def custom_sql_call(self, sql):
        return self.conn.execute(sql)