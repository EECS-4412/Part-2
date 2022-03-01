from matplotlib import projections
from clients.SqliteClient import SqlClient
import numpy as np
import matplotlib.pyplot as plt



def part4():
    # sql_client = SqlClient(os.environ["DB_PATH"])
    sql_client = SqlClient()
    rows = sql_client.custom_sql_call('''
    SELECT
        HEIGHT, WEIGHT
    FROM
        player_attributes
    ''').fetchall()

    mat = np.array([list(x) for x in rows if all(x)])
    means = np.mean(mat.T, axis=1)
    stds = np.std(mat.T, axis=1)

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            mat[i][j] = (mat[i][j] - means[j])/stds[j]

    covariance = np.cov(mat.T)

    eigenvalues, eigenvectors = np.linalg.eig(covariance)


    projection = eigenvectors.T.dot(covariance.T)
    print(projection)

    heights = mat[:,0]
    weights = mat[:,1]
    plt.scatter(heights, weights, s=5)
    plt.title(f'Player Height Vs Weight with Principle Components overlayed')
    plt.xlabel("Player Heights, Z-Score standardized")
    plt.ylabel("Player Weights, Z-Score standardized")
    plt.quiver(0,0, projection[0][0], projection[0][1], color='r', scale=5)
    plt.quiver(0,0, projection[1][0], projection[1][1], color='b', scale=5)
    plt.savefig(f'graphs/part4_g1.png')
    plt.clf()

    # conclusions:
    # if you look at the graph, you will see that there is a very strong coorelation between height and weight
    # and a very week orthogonal coorelation




    return
