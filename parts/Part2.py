from clients.SqliteClient import SqlClient
import numpy as np
import os

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
    # PREPROCESSING STEP: select value only for Toronto's points
    points_per_game = [x[0] if "Toronto" in x[2] else x[1] for x in rows]
    arithmetic_mean = np.mean(points_per_game)
    geometric_mean = np.exp(np.log(points_per_game).mean())
    harmonic_mean = len(points_per_game)/sum([1/x for x in points_per_game])
    print(f'arithmetic mean: {arithmetic_mean}')
    print(f'geometric mean: {geometric_mean}')
    print(f'harmonic mean: {harmonic_mean}')



    return