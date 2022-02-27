import csv
from clients.SqliteClient import SqlClient
from scipy.spatial import distance
import numpy as np
import os

def part5():
    sql_client = SqlClient(db_path=os.environ["DB_PATH"])
    rows = sql_client.custom_sql_call('''
    SELECT
        HEIGHT, WEIGHT, PTS, AST, REB
    FROM
        player_attributes
    LIMIT
        20
    ''').fetchall()

    rows = np.array([x for x in rows if all(x)][:10])
    mean = np.mean(rows.T, axis=1)
    std = np.std(rows.T, axis=1)
    
    # Z-score standardized data for more meaningful distances
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            rows[i][j] = (rows[i][j] - mean[j])/std[j]
        

    pairs = []
    euclidean_distances = []
    cosine_distances = []
    mahalanobis_distances = []
    cov = np.cov(np.array([list(x) for x in rows if all(x)]).T)
    for i in range(0,10):
        for j in range(i + 1, 10):
            pairs.append((i,j))
            euclidean_distances.append(distance.euclidean(rows[i], rows[j]))
            cosine_distances.append(distance.cosine(rows[i], rows[j]))
            mahalanobis_distances.append(distance.mahalanobis(rows[i], rows[j], cov))

    with open(f'csv/215659501-215528797-215494925-T5ITEMS.csv', 'w') as f:
        f.write('ENTRY_NUMBER,HEIGHT,WEIGHT,PTS,AST,REB\n')
        w = csv.writer(f,delimiter=',')
        for i, row in enumerate(rows):
            w.writerow([i] + list(row))


    with open(f'csv/215659501-215528797-215494925-T5EU.csv', 'w') as f:
        f.write('PAIR,EUCLIDEAN_DISTANCE\n')
        w = csv.writer(f,delimiter=',')
        for row in zip(pairs, euclidean_distances):
            w.writerow(row)

    with open(f'csv/215659501-215528797-215494925-T5CO.csv', 'w') as f:
        f.write('PAIR,COSINE_DISTANCE\n')
        w = csv.writer(f,delimiter=',')
        for row in zip(pairs, cosine_distances):
            w.writerow(row)

    with open(f'csv/215659501-215528797-215494925-T5MA.csv', 'w') as f:
        f.write('PAIR,MAHALANOBIS_DISTANCE\n')
        w = csv.writer(f,delimiter=',')
        for row in zip(pairs, mahalanobis_distances):
            w.writerow(row)

    return
