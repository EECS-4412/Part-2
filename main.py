import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3 as sql


def get_players(conn, num_players):
    rows = conn.execute(
        '''
    SELECT * FROM player LIMIT {num_players}
    '''.format(num_players=num_players))

    for row in rows:
        print(row)


if __name__ == "__main__":
    conn = sql.connect('./kaggle/input/basketball/basketball.sqlite')
    get_players(conn, 5)
