import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3 as sql
import os
from datetime import datetime
import matplotlib.pyplot as plot

from clients.SqliteClient import SqlClient

def testing():
    sql_client = SqlClient(os.environ["DB_PATH"])
    # top_salaries()
    # min_salaries()
    # avg_salaries()
    # player_ages()
    # player_country()
    # team_win_loss_home()
    # team_with_1st_draft()
    # sql_client.top_1st_draft()
    [print(x) for x in sorted(sql_client.custom_sql_call("PRAGMA table_info(game);"), key=lambda x: x[1])]

    rows = sql_client.custom_sql_call("""
    SELECT 
        WL_HOME, WL_AWAY, HOME_TEAM_WINS, HOME_TEAM_LOSSES, PTS_HOME, PTS_AWAY, TEAM_NAME_HOME, TEAM_NAME_AWAY, GAME_DATE
    FROM 
        game
    """)

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




def part1():
    sql_client = SqlClient(os.environ["DB_PATH"])
    return

def part2():
    return

def part3():
    return

def part4():
    return

def part5():
    return

def part6():
    return

def part7():
    return

def main():
    part1()
    part2()
    part3()
    part4()
    part5()
    part6()
    part7()


if __name__ == "__main__":
    #main()
    testing()
