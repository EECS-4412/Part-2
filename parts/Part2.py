from clients.SqliteClient import SqlClient
import numpy as np
from datetime import datetime
import csv
from collections import Counter


def part2():
    # sql_client = SqlClient(os.environ["DB_PATH"])
    sql_client = SqlClient("./kaggle/input/basketball/basketball.sqlite")
    # NOMINAL
    #
    rows = sql_client.custom_sql_call('''
    SELECT
        COUNTRY
    FROM
        player_attributes
    ''')
    countries = []
    with open(f'csv/215659501-215528797-215494925-T2-1.csv', 'w') as f:
        f.write(f'COUNTRY\n')
        w = csv.writer(f, delimiter=',')
        for row in rows:
            w.writerow(row)
            countries.append(row[0])

    countries_freq = Counter(countries)
    most_common = countries_freq.most_common(1)[0]
    print(f'most common country of origin: {most_common}')
    # ORDINAL
    #   Player birth dates
    rows = sql_client.custom_sql_call('''
    SELECT
        BIRTHDATE
    FROM
        player JOIN player_attributes ON Player.id = Player_Attributes.ID
    WHERE
        IS_ACTIVE=1
    ''')

    birthdates = []
    with open(f'csv/215659501-215528797-215494925-T2-2.csv', 'w') as f:
        f.write(f'BIRTHDATE\n')
        w = csv.writer(f, delimiter=',')
        for row in rows:
            w.writerow(row)
            birthdates.append(datetime.strptime(
                row[0].split("T")[0], "%Y-%m-%d"))

    average_date = datetime.utcfromtimestamp(
        sum([datetime.timestamp(x) for x in birthdates])//len(birthdates))
    median_date = sorted(birthdates)[len(birthdates)//2]
    print(f'Average birthdate is: {average_date}')
    print(f'median birthdate is: {median_date}')

    # INTERVAL
    #   Toronto home and away points
    rows = sql_client.custom_sql_call('''
    SELECT
        PLUS_MINUS_HOME, PLUS_MINUS_AWAY, TEAM_NAME_HOME, TEAM_NAME_AWAY
    FROM
        game
    WHERE
       TEAM_NAME_HOME="Toronto Huskies" OR TEAM_NAME_HOME="Toronto Raptors" OR TEAM_NAME_AWAY="Toronto Huskies" OR TEAM_NAME_AWAY="Toronto Raptors"
    ''')
    toronto_home = []
    toronto_away = []
    with open(f'csv/215659501-215528797-215494925-T2-3.csv', 'w') as f:
        f.write(f'PLUS_MINUS_HOME,PLUS_MINUS_AWAY,TEAM_NAME_HOME,TEAM_NAME_AWAY\n')
        for pm_home, pm_away, tn_home, tn_away in rows:
            w = csv.writer(f, delimiter=',')
            w.writerow((pm_home, pm_away, tn_home, tn_away))
            if 'Toronto' in tn_home:
                toronto_home.append(pm_home)
            else:
                toronto_away.append(pm_away)

    mean_home = np.mean(toronto_home)
    std_home = np.std(toronto_home)
    mean_away = np.mean(toronto_away)
    std_away = np.std(toronto_away)
    print(f'mean home: {mean_home}, standard deviation home: {std_home}')
    print(f'mean away: {mean_away}, standard deviation away: {std_away}')

    # RATIO
    #   HOW MANY POINTS DID TORONTO SCORE PER GAME
    rows = sql_client.custom_sql_call('''
    SELECT
        PTS_HOME, PTS_AWAY, TEAM_NAME_HOME, TEAM_NAME_AWAY, GAME_DATE
    FROM
        game
    WHERE
        TEAM_NAME_HOME="Toronto Huskies" OR TEAM_NAME_HOME="Toronto Raptors" OR TEAM_NAME_AWAY="Toronto Huskies" OR TEAM_NAME_AWAY="Toronto Raptors"
    ''')
    # PREPROCESSING STEP: select value only for The team with Toronto in its name
    points_per_game = []
    with open(f'csv/215659501-215528797-215494925-T2-4.csv', 'w') as f:
        f.write(f'PTS_HOME,PTS_AWAY,TEAM_NAME_HOME,TEAM_NAME_AWAY,GAME_DATE\n')
        for pts_home, pts_away, team_name_home, team_name_away, game_date in rows:
            w = csv.writer(f, delimiter=',')
            w.writerow((pts_home, pts_away, team_name_home,
                       team_name_away, game_date))
            points_per_game.append(
                pts_home if "Toronto" in team_name_home else pts_away)

    arithmetic_mean = np.mean(points_per_game)
    geometric_mean = np.exp(np.log(points_per_game).mean())
    harmonic_mean = len(points_per_game)/sum([1/x for x in points_per_game])
    print(f'arithmetic mean: {arithmetic_mean}')
    print(f'geometric mean: {geometric_mean}')
    print(f'harmonic mean: {harmonic_mean}')

    return
