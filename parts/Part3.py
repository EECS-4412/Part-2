from clients.SqliteClient import SqlClient
import numpy as np
import csv
import matplotlib.pyplot as plt
from datetime import datetime

def scatter_plot(x, x_name, y, y_name, titleName, filename):
    plt.scatter(x, y, s=5)
    plt.title(f'{titleName}')
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.savefig(f'graphs/{filename}.png')
    plt.clf()


def part3():
    # sql_client = SqlClient(os.environ["DB_PATH"])
    sql_client = SqlClient()
    # Interval data
    #   Re using the plus minus home/away data
    rows = sql_client.custom_sql_call('''
    SELECT
        PLUS_MINUS_HOME, PLUS_MINUS_AWAY, TEAM_NAME_HOME, TEAM_NAME_AWAY, GAME_DATE
    FROM
        game
    WHERE
       (TEAM_NAME_HOME="Toronto Huskies" OR
       TEAM_NAME_HOME="Toronto Raptors" OR
       TEAM_NAME_AWAY="Toronto Huskies" OR
       TEAM_NAME_AWAY="Toronto Raptors") AND
       GAME_DATE > 19900101
    ''').fetchall()
    toronto_home = []
    toronto_away = []
    game_dates_home = []
    game_dates_away = []
    for pm_home, pm_away, tn_home, _, game_date in rows:
        if 'Toronto' in tn_home:
            toronto_home.append(pm_home)
            game_dates_home.append(datetime.strptime(game_date.split("T")[0], "%Y-%m-%d"))
        else:
            toronto_away.append(pm_away)
            game_dates_away.append(datetime.strptime(game_date.split("T")[0], "%Y-%m-%d"))

    mean_home = np.mean(toronto_home)
    std_home = np.std(toronto_home)
    toronto_home_z_score = [(x - mean_home)/std_home for x in toronto_home]
    min_home_val, max_home_val = min(toronto_home), max(toronto_home)
    min_max_home_normalized = [(x - min_home_val)/ (max_home_val - min_home_val)  for x in toronto_home]

    mean_away = np.mean(toronto_away)
    std_away = np.std(toronto_away)
    toronto_away_z_score = [(x - mean_away)/std_away for x in toronto_away]
    min_away_val, max_away_val = min(toronto_away), max(toronto_away)
    min_max_away_normalized = [(x - min_away_val)/ (max_away_val - min_away_val)  for x in toronto_away]
    with open(f'csv/215659501-215528797-215494925-T3-1.csv', 'w') as f:
        f.write(f'HOME_OR_AWAY,PLUS_MINUS,Z_SCORE_NORMALIZED,MIN_MAX_NORMALIZED\n')
        w = csv.writer(f,delimiter=',')
        for org, zs, mm in zip(toronto_home, toronto_home_z_score, min_max_home_normalized):
            w.writerow(('home',org, zs, mm))

        for org, zs, mm in zip(toronto_away, toronto_away_z_score, min_max_away_normalized):
            w.writerow(('away',org, zs, mm))

    scatter_plot(game_dates_home, "Date of game", toronto_home, "Plus minus Home", "Plus minus home vs date of game", 'part3_g1')
    scatter_plot(game_dates_home, "Date of game", toronto_home_z_score, "Plus minus Home Z score", "Plus minus home Z score vs date of game", 'part3_g2')
    scatter_plot(game_dates_home, "Date of game", min_max_home_normalized, "Plus minus Home min max normalized", "Plus minus home min max normalized vs date of game", 'part3_g3')
    scatter_plot(game_dates_away, "Date of game", toronto_away, "Plus minus Away", "Plus minus away vs date of game", 'part3_g4')
    scatter_plot(game_dates_away, "Date of game", toronto_away_z_score, "Plus minus Away Z score", "Plus minus away Z score vs date of game", 'part3_g5')
    scatter_plot(game_dates_away, "Date of game", min_max_away_normalized, "Plus minus Away min max normalized", "Plus minus away min max normalized vs date of game", 'part3_g6')

    rows = sql_client.custom_sql_call('''
    SELECT
        HEIGHT, WEIGHT
    FROM
        PLAYER_ATTRIBUTES
    ''').fetchall()
    heights, weights = [], []
    for h, w in rows:
        if h and w:
            heights.append(h)
            weights.append(w)

    heights_mean = np.mean(heights)
    heights_std = np.std(heights)
    heights_z_score = [(x - heights_mean)/heights_std for x in heights]
    weights_mean = np.mean(weights)
    weights_std = np.std(weights)
    weights_z_score = [(x - weights_mean)/weights_std for x in weights]
    heights_min, heights_max = min(heights), max(heights)
    weights_min, weights_max = min(weights), max(weights)
    heights_min_max = [(x - heights_min)/(heights_max - heights_min) for x in heights]
    weights_min_max = [(x - weights_min)/(weights_max - weights_min) for x in weights]
    with open(f'csv/215659501-215528797-215494925-T3-2.csv', 'w') as f:
        f.write(f'HEIGHT,HEIGHT_ZSCORE,HEIGHT_MIN_MAX,WEIGHT,WEIGHT_ZSCORE,WEIGHT_MIN_MAX\n')
        w = csv.writer(f,delimiter=',')
        for height, height_z, height_mm, weight, weight_z, weight_mm in zip(heights, heights_z_score, heights_min_max, weights, weights_z_score, weights_min_max):
            w.writerow((height, height_z, height_mm, weight, weight_z, weight_mm))


    scatter_plot(heights, "Player Height", weights, "Player Weight", "Player Weight vs Player Height", 'part3_g7')
    scatter_plot(heights_z_score, "Player Height Z Score", weights_z_score, "Player Weight Z Score", "Player Weight Z Score vs Player Height Z Score", 'part3_g8')
    scatter_plot(heights_min_max, "Player Height Min Max Normalized", weights_min_max, "Player Weight Min Max Normalized", "Player Weight Min Max Normalized vs Player Height Min Max Normalized", 'part3_g9')
    return
