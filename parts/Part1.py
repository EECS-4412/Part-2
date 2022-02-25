import matplotlib.pyplot as plt
from matplotlib import cm
from clients.SqliteClient import SqlClient
import os
from collections import Counter
import numpy as np

def part1():
    sql_client = SqlClient(os.environ["DB_PATH"])
    average_salaries_plot(sql_client)
    first_draft_plot(sql_client)    
    player_country_plot(sql_client)
    player_ages_plot(sql_client)
    player_height_plot(sql_client)

def player_height_plot(sql_client):
    year, height = list(zip(*player_height(sql_client)))
    plt.ylim(75, 80)
    bar_plot(height[::-1], 'Player Height (Inches)', year[::-1], 'Draft Year', "Player Height at Draft", 'player_height')

def player_ages_plot(sql_client):
    year, num_players = list(zip(*player_ages(sql_client)))
    bar_plot(num_players[::-1], 'Number Of Players', year[::-1], 'Year Born', "Player Age Per Year", 'player_age')

def average_salaries_plot(sql_client):
    season, salaries = list(zip(*avg_salaries(sql_client)))
    scatter_plot(season, 'Season', salaries, 'Average Salaries', 'Average Salary Per Season', 'average_salaries')

def first_draft_plot(sql_client):
    year, team = list(zip(*team_with_1st_draft(sql_client)))
    count = Counter(team)
    name, freq = list(zip(*[(name, freq) for name, freq in count.most_common()]))
    name = list(name)
    freq = list(freq)
    ones = sum([1 for f in freq if f == 1])
    name = name[:-ones]
    name.append('Other (teams with only one pick)')
    freq = freq[:-ones]
    freq.append(ones)
    pie_plot(freq, name, 'First Round Picks', 'first_round_picks')

def player_country_plot(sql_client):
    _countries, _counts = list(zip(*player_country(sql_client)))
    countries, counts = list(_countries), list(_counts)
    others_size = len([c for c in _counts if c <= 10])
    counts, countries = counts[:-others_size], countries[:-others_size]
    countries.append('Other (Countries < 10 players all grouped here)')
    counts.append(others_size)
    pie_plot(counts, countries, 'Player Countries', 'player_countries')
    pie_plot(counts[1:], countries[1:], 'Player Countries (no USA)', 'player_countries_no_usa')

'''
Below functions facilitate 
'''
def scatter_plot(x, x_name, y, y_name, titleName, filename):
    plt.scatter(x, y, s=5)
    plt.title(f'{titleName}')
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.savefig(f'graphs/{filename}.png')
    plt.clf()

def pie_plot(freq, labels, titleName, filename):
    cs = cm.tab20b(np.arange(len(freq))/len(freq))
    patches, _ = plt.pie(freq, colors=cs, startangle=90)
    new_labels = [', '.join([lab, str(fre)]) for (lab, fre) in zip(labels, freq)]
    plt.legend(patches, new_labels, loc="best", bbox_to_anchor=(1.02, 1))
    plt.title(f'{titleName}')
    plt.savefig(f'graphs/{filename}.png', bbox_inches='tight')
    plt.clf()

def bar_plot(data, data_name, labels, labels_name, titleName, filename):
    plt.bar(labels, data)
    plt.xticks(fontsize=6)
    plt.title(f'{titleName}')
    plt.ylabel(data_name)
    plt.xlabel(labels_name)
    plt.savefig(f'graphs/{filename}.png')
    plt.clf()
    
'''
Returns number of active players
'''
def number_active_players(client, num_players):
    rows = client.custom_sql(
    '''
    SELECT count(id) as num_players FROM player WHERE is_active=1
    '''.format(num_players=num_players))

    return rows.fetchall()

'''
Return all players
'''
def get_players(client, num_players):
    rows = client.custom_sql_call(
        '''
        SELECT * FROM player LIMIT {num_players}
        '''.format(num_players=num_players)
    )

    return rows.fetchall()

'''
Returns top salaries with entries (season, name, team, salary)
'''
def top_salaries(client):
    rows = client.custom_sql_call(
        '''
        SELECT slugSeason, namePlayer, nameTeam, MAX(value) as salary
        FROM player_salary 
        GROUP BY slugSeason
        '''
    )

    return rows.fetchall()

'''
Returns min salaries with entries (season, name, team, salary)
'''
def min_salaries(client):
    rows = client.custom_sql_call(
        '''
        SELECT slugSeason, namePlayer, nameTeam, MIN(value) as salary
        FROM player_salary 
        GROUP BY slugSeason
        '''
    )

    return rows.fetchall()

'''
Return average salaries with entries (season, salary)
'''
def avg_salaries(client):
    rows = client.custom_sql_call(
        '''
        SELECT slugSeason, AVG(value) as salary
        FROM player_salary 
        GROUP BY slugSeason
        '''
    )

    return rows.fetchall()

'''
Return number of players born per year with entries (birth_year, num_players)
'''
def player_ages(client):
    # ACTIVE PLAYERS BY YEAR
    rows = client.custom_sql_call(
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
        '''
    )

    # ACTIVE PLAYERS HISTORICALLY
    # rows = client(
    #     '''
    # SELECT strftime('%Y', birthdate), COUNT(strftime('%Y', birthdate)) AS num_players
    # FROM player_attributes
    # GROUP BY strftime('%Y', birthdate)
    # ORDER BY strftime('%Y', birthdate) DESC
    # ''')

    return rows.fetchall()

'''
Number of Players per country with entries (Country, num_players)
'''
def player_country(client):
    rows = client.custom_sql_call(
        '''
        SELECT Country, count(*)
        FROM player JOIN player_attributes ON Player.id = Player_Attributes.ID
        GROUP BY Country
        ORDER BY count(*) DESC
        '''
    )

    return rows.fetchall()

'''
Team win/loss ration at home with entries (team_name, num_home_games, home_win, home_loss, wl_ratio, year)
'''
def team_win_loss_home(client):
    rows = client.custom_sql_call(
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
        '''
    )

    return rows.fetchall()

'''
Team with 1st overall draft by year with entries (year, team)
'''
def team_with_1st_draft(client):
    rows = client.custom_sql_call(
        '''
    SELECT yearDraft, nameTeam
    FROM draft
    WHERE numberPickOverall = 1
    ORDER BY yearDraft DESC
    ''')

    return rows.fetchall()

'''
Team total 1st overall draft (team count)
'''
def top_1st_draft(client):
    rows = client.custom_sql_call(
        '''
        SELECT nameTeam, COUNT(nameTeam) as count
        FROM draft
        WHERE numberPickOverall = 1
        GROUP BY nameTeam
        ORDER BY count DESC
        '''
    )

    return rows.fetchall()

def player_height(client):
    rows = client.custom_sql_call(
        '''
        SELECT yearCombine, AVG(heightWOShoesInches)
        FROM Draft_Combine
        GROUP BY yearCombine
        '''
    )

    return rows.fetchall()
if __name__ == '__main__':
    part1()