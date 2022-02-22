import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import sqlite3 as sql


def number_active_players(conn):
    rows = conn.execute(
        '''
    SELECT count(id) as num_players FROM player WHERE is_active=1
    '''.format(num_players=num_players))

    print('\nNUM ACTIVE PLAYERS\n---------')
    for row in rows:
        print(row)


def get_players(conn, num_players):
    rows = conn.execute(
        '''
    SELECT * FROM player LIMIT {num_players}
    '''.format(num_players=num_players))

    for row in rows:
        print(row)


def top_salaries(conn):
    rows = conn.execute(
        '''
    SELECT slugSeason, namePlayer, nameTeam, MAX(value) as salary
    FROM player_salary 
    GROUP BY slugSeason
    ''')

    print('\nTOP SALARIES (season, name, team, salary)')
    for row in rows:
        print(row)


def min_salaries(conn):
    rows = conn.execute(
        '''
    SELECT slugSeason, namePlayer, nameTeam, MIN(value) as salary
    FROM player_salary 
    GROUP BY slugSeason
    ''')

    print('\nMIN SALARIES (season, name, team, salary)')
    for row in rows:
        print(row)


def avg_salaries(conn):
    rows = conn.execute(
        '''
    SELECT slugSeason,  AVG(value) as salary
    FROM player_salary 
    GROUP BY slugSeason
    ''')

    print('\nAVG SALARIES (season, salary)')
    for row in rows:
        print(row)


def player_ages(conn):
    # ACTIVE PLAYERS BY YEAR
    rows = conn.execute(
        '''
    SELECT strftime('%Y', birthdate), COUNT(strftime('%Y', birthdate)) AS num_players
    FROM (
        SELECT * 
        FROM player
        WHERE is_active = 1
        ) p
    INNER JOIN player_attributes pa ON pa.id = p.id   
    GROUP BY strftime('%Y', birthdate)
    ORDER BY strftime('%Y', birthdate) DESC
    ''')

    # ACTIVE PLAYERS HISTORICALLY
    # rows = conn.execute(
    #     '''
    # SELECT strftime('%Y', birthdate), COUNT(strftime('%Y', birthdate)) AS num_players
    # FROM player_attributes
    # GROUP BY strftime('%Y', birthdate)
    # ORDER BY strftime('%Y', birthdate) DESC
    # ''')

    print('\nNUM PLAYERS PER BIRTH YEAR (season, num_players)')
    for row in rows:
        print(row)


def player_country(conn):
    rows = conn.execute(
        '''
   SELECT Country, count(*)
    FROM player JOIN player_attributes ON Player.id = Player_Attributes.ID
    GROUP BY Country
    ORDER BY count(*) DESC
    ''')

    print('\nNumber of players per Country (Country, num_players)')
    for row in rows:
        print(row)


def team_win_loss_home(conn):
    rows = conn.execute(
        '''
    SELECT TEAM_NAME_HOME as TEAM_NAME,
       count(WL_HOME) as HOME_GAME_AMOUNT,
       count(CASE WHEN WL_HOME = 'W' THEN 1 END) as HOME_WINS,
       count(CASE WHEN WL_HOME = 'L' THEN 1 END) as HOME_LOSES,
       ROUND(
           (CAST(count(CASE WHEN WL_HOME = 'W' THEN 1 END) as FLOAT) / CAST(count(WL_HOME) as FLOAT)) * 100,
           2
       ) as WL_RATIO,
       SUBSTR(Game.GAME_DATE, 0, 5) as YEAR
FROM Game
GROUP BY TEAM_NAME_HOME, Year
    ''')

    print('\nTeam win/loss ratio at home (team_name, num_home_games, home_win, home_loss, wl_ratio, year)')
    for row in rows:
        print(row)


def team_with_1st_draft(conn):
    rows = conn.execute(
        '''
    SELECT yearDraft, nameTeam
    FROM draft
    WHERE numberPickOverall = 1
    ORDER BY yearDraft DESC
    ''')

    print('\nTEAM WITH 1st OVERALL DRAFT by YEAR (year, team)\n----------------------------------------')
    for row in rows:
        print(row)


def top_1st_draft(conn):
    rows = conn.execute(
        '''
    SELECT nameTeam, COUNT(nameTeam) as count
    FROM draft
    WHERE numberPickOverall = 1
    GROUP BY nameTeam
    ORDER BY count DESC
    ''')

    print('\nTEAM TOTAL 1st OVERALL DRAFT (team, count)\n----------------------------------------')
    for row in rows:
        print(row)


if __name__ == "__main__":
    conn = sql.connect('./kaggle/input/basketball/basketball.sqlite')
    # top_salaries(conn)
    # min_salaries(conn)
    # avg_salaries(conn)
    # player_ages(conn)
    # player_country(conn)
    # team_win_loss_home(conn)
    # team_with_1st_draft(conn)
    top_1st_draft(conn)
