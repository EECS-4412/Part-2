import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3 as sql
import os

from clients.SqliteClient import SqlClient


if __name__ == "__main__":
    sql_client = SqlClient(os.environ["DB_PATH"])
    # top_salaries(conn)
    # min_salaries(conn)
    # avg_salaries(conn)
    # player_ages(conn)
    # player_country(conn)
    # team_win_loss_home(conn)
    # team_with_1st_draft(conn)
    sql_client.top_1st_draft()
    [print(x) for x in sql_client.custom_sql_call("""
    SELECT 
    name
FROM 
    sqlite_master
WHERE 
    type ='table' AND 
    name NOT LIKE 'sqlite_%';
    """)]
