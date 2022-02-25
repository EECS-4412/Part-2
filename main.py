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




def part1():
    sql_client = SqlClient(os.environ["DB_PATH"])
    return

def part2():
    sql_client = SqlClient(os.environ["DB_PATH"])
    # NOMINAL
    #
    # ORDINAL
    #
    # INTERVAL
    #   
    # RATIO
    #   HOW MANY POINTS DID TORONTO SCORE PER GAME
    rows = sql_client.custom_sql_call("""
    SELECT 
        PTS_HOME, PTS_AWAY, TEAM_NAME_HOME, TEAM_NAME_AWAY, GAME_DATE
    FROM 
        game
    WHERE
        TEAM_NAME_HOME="Toronto Huskies" OR TEAM_NAME_HOME="Toronto Raptors" OR TEAM_NAME_AWAY="Toronto Huskies" OR TEAM_NAME_AWAY="Toronto Raptors"
    """)

    points_per_game = [x[0] if "Toronto" in x[2] else x[1] for x in rows]
    # fancy python call
    # basically calculates geometric mean using logs to avoid exhaustively large numbers
    arithmetic_mean = np.mean(points_per_game)
    geometric_mean = np.exp(np.log(points_per_game).mean())
    harmonic_mean = len(points_per_game)/sum([1/x for x in points_per_game])
    print(f'arithmetic mean: {arithmetic_mean}')
    print(f'geometric mean: {geometric_mean}')
    print(f'harmonic mean: {harmonic_mean}')



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
    main()
    #testing()
