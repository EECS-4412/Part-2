import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3 as sql
import os
from datetime import datetime
import matplotlib.pyplot as plot
import traceback
from parts.Part1 import part1
from parts.Part2 import part2
from parts.Part3 import part3
from parts.Part4 import part4
from parts.Part5 import part5
from parts.Part6 import part6

from dotenv import load_dotenv

load_dotenv()

from clients.SqliteClient import SqlClient

def testing():
    sql_client = SqlClient(os.environ["DB_PATH"])
    [print(x) for x in sorted(sql_client.custom_sql_call("PRAGMA table_info(game);"), key=lambda x: x[1])]

    rows = sql_client.custom_sql_call("""
    SELECT
        WL_HOME, WL_AWAY, HOME_TEAM_WINS, HOME_TEAM_LOSSES, PTS_HOME, PTS_AWAY, TEAM_NAME_HOME, TEAM_NAME_AWAY, GAME_DATE
    FROM
        game
    """)

    rows = sql_client.custom_sql_call("""
    SELECT
        TEAM_NAME_HOME, TEAM_NAME_AWAY
    FROM
        game
    """)

    all_teams = []
    [all_teams.extend([x[0], x[1]]) for x in rows]
    all_teams = sorted(list(set(all_teams)))
    [print(x) for x in all_teams]

    return

    # number of points it takes to win a game
    winning_points = [(x[4] if x[0] == "W" else x[5], datetime.strptime(x[-1], "%Y-%m-%d")) for x in rows]
    winning_points.sort(key=lambda x:x[1])
    x = [x[1] for x in winning_points]
    y = [x[0] for x in winning_points]

    plot.plot(x,y)
    plot.xlabel("Date/Year")
    plot.ylabel("Points to win game")
    plot.savefig('test.png')
    plot.clf()


def main():
    methods = [
        part1,
        part2,
        part3,
        part4,
        part5,
        part6,
    ]
    for method in methods:
        try:
            method()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            print(f'{method.__name__} done ❌')
            continue
        print(f'{method.__name__} done ✅')


if __name__ == "__main__":
    main()
