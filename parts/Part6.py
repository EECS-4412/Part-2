from clients.SqliteClient import SqlClient
import os
from sklearn import tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


def part6():
    """
        possible positions (from db)
        Forward
        Center
        Guard
        Forward-Guard
        Center-Forward
        NULL


    """

    # sql_client = SqlClient(os.environ["DB_PATH"])
    sql_client = SqlClient("./kaggle/input/basketball/basketball.sqlite")
    rows = sql_client.custom_sql_call('''
    SELECT
         PTS, AST, REB, HEIGHT, WEIGHT, POSITION
    FROM
        player JOIN player_attributes ON Player.id = Player_Attributes.ID
    WHERE
        IS_ACTIVE=1 AND
        HEIGHT IS NOT NULL AND
        WEIGHT IS NOT NULL AND
        PTS IS NOT NULL AND
        AST IS NOT NULL AND
        REB IS NOT NULL;
    ''').fetchall()

    labels = [x[5].split('-')[-1] for x in rows]
    rows = np.array([x[0:5] for x in rows])
    mean = np.mean(rows.T, axis=1)
    std = np.std(rows.T, axis=1)

    # Z-score standardized data for more meaningful distances
    # for i in range(len(rows)):
    #     for j in range(len(rows[0])):
    #         rows[i][j] = (rows[i][j] - mean[j])/std[j]

    # DECISION TREE CLASSIFIER

    dtc_gini = tree.DecisionTreeClassifier(
        criterion="gini",
        splitter="best",
        max_depth=4,
        # min_samples_split=10,
        # min_samples_leaf=10,
        # min_weight_fraction_leaf=0.0,
        # max_features="auto",
        # max_features=None,
        max_leaf_nodes=12
    )
    attributes = [x[0:5] for x in rows]
    # print(Counter(labels))

    X_train, X_test, y_train, y_test = train_test_split(
        attributes, labels, test_size=0.33, random_state=42)

    dtc_gini.fit(X_train, y_train)

    dtc_entropy = tree.DecisionTreeClassifier(
        criterion="entropy",
        splitter="best",
        max_depth=4,
        # min_samples_split=10,
        # min_samples_leaf=10,
        # min_weight_fraction_leaf=0.0,
        # max_features="auto",
        # max_features=None,
        max_leaf_nodes=12
    )
    dtc_entropy.fit(X_train, y_train)

    fig = plt.figure(figsize=(25, 20))
    _ = tree.plot_tree(dtc_gini,
                       feature_names=["PTS", "AST", "REB", "HEIGHT", "WEIGHT"],
                       class_names=['Center', 'Forward', 'Guard'],
                       filled=True)
    fig.savefig("graphs/decision_tree_gini.png")

    fig = plt.figure(figsize=(25, 20))
    _ = tree.plot_tree(dtc_entropy,
                       feature_names=["PTS", "AST", "REB", "HEIGHT", "WEIGHT"],
                       class_names=['Center', 'Forward', 'Guard'],
                       #    class_names=['Center',  'Center-Forward', 'Forward', 'Forward-Center','Forward-Guard', 'Guard', 'Guard-Forward'],
                       filled=True)
    fig.savefig("graphs/decision_tree_entropy.png")

    print("[GINI]    Decision Tree - Train:", dtc_gini.score(X_train, y_train))
    print("[GINI]    Decision Tree - Test :", dtc_gini.score(X_test, y_test))
    print("[ENTROPY] Decision Tree - Train:",
          dtc_entropy.score(X_train, y_train))
    print("[ENTROPY] Decision Tree - Test :",
          dtc_entropy.score(X_test, y_test))

    # RULE BASE CLASSIFIER

    rows = sql_client.custom_sql_call('''
    SELECT
         PTS, AST, REB, HEIGHT, WEIGHT, POSITION
    FROM
        player JOIN player_attributes ON Player.id = Player_Attributes.ID
    WHERE
        IS_ACTIVE=1 AND
        HEIGHT IS NOT NULL AND
        WEIGHT IS NOT NULL AND
        PTS IS NOT NULL AND
        AST IS NOT NULL AND
        REB IS NOT NULL;
    ''').fetchall()

    first_or_last = 0

    totals = Counter([x[5].split('-')[first_or_last] for x in rows])
    print(totals)
    results = {}
    counts = {}

    for height_thresh in range(70, 84, 1):
        height_thresh = height_thresh
        for weight_thresh in range(190, 240, 5):
            for weight_plus in range(0, 40*2, 5):
                weight_plus = weight_plus / 2
                for pts_thresh in range(10, 20, 2):
                    for pts_plus in range(10, 20, 2):
                        classes = {
                            'Guard': [],
                            'Forward': [],
                            'Center': [],
                            'Unclassified': []
                        }
                        #PTS, AST, REB, HEIGHT, WEIGHT, POSITION
                        for pts, ast, reb, height, weight, position in rows:
                            position = position.split('-')[first_or_last]
                            if height <= height_thresh and weight <= weight_thresh and pts <= pts_thresh:
                                classes['Guard'].append(position)
                            elif height <= height_thresh and weight <= weight_thresh and pts > pts_thresh:
                                classes['Forward'].append(position)
                            elif height <= height_thresh and weight > weight_thresh:
                                classes['Forward'].append(position)
                            elif height > height_thresh and weight <= weight_thresh + weight_plus:
                                classes['Forward'].append(position)
                            elif height > height_thresh and weight > weight_thresh + weight_plus and pts > pts_thresh + pts_plus:
                                classes['Forward'].append(position)
                            elif height > height_thresh and weight > weight_thresh + weight_plus and pts <= pts_thresh + pts_plus:
                                classes['Center'].append(position)
                            else:
                                print('unclassy')
                                classes['Unclassified'].append(position)

                        acc = {}
                        count_local = {}

                        for key, value in classes.items():
                            correct = [x for x in value if x == key]
                            if len(value) > 0:
                                acc[key] = len(correct)/totals[key]
                            count_local[key] = Counter(value)

                    results[(height_thresh, weight_thresh,
                             weight_plus, pts_thresh, pts_plus)] = acc
                    counts[(height_thresh, weight_thresh, weight_plus,
                            pts_thresh, pts_plus)] = count_local

    # print(results)
    # print(list(results.keys())[0])
    # print(list(results.values())[0])
    # print(len(results))
    # print(len([x for x in results.values() if "Guard" in x.keys()]))
    max_val, max_key = 0, None
    for key, value in results.items():
        if sum(list(value.values())) > max_val:
            max_key = key
            max_val = sum(list(value.values()))

    print(max_val)
    print(max_key)
    print(results[max_key])
    print(counts[max_key])
    # print(Counter(classes['Unclassified']))

    # height
    # -------------------------
    # |           |           |
    # |           |           |
    # -------------------------
    # |           |           |
    # |           |           |
    # -------------------------

    return
