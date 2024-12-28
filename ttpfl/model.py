import csv
import pulp
import sys

def get_player_data(wta_file, atp_file):
    players = []
    points = []
    prices = []
    tours = []

    players, points, prices, tours = read_file_data(wta_file, 'wta')
    players2, points2, prices2, tours2 = read_file_data(atp_file, 'atp')

    players.extend(players2)
    points.extend(points2)
    prices.extend(prices2)
    tours.extend(tours2)

    return players, points, prices, tours

def read_file_data(file, tour):
    players = []
    points = []
    prices = []
    tours = []

    with open(file, newline='', encoding='latin1') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            players.append(row[0])
            points.append(int(row[1]))
            prices.append(int(row[2]))
            tours.append(tour)

    return players, points, prices, tours

def run_model(expected_points, prices, tours):
    model = pulp.LpProblem("TTPFL", pulp.LpMaximize)

    num_players = len(expected_points)

    decisions = [
        pulp.LpVariable("x{}".format(i), cat=pulp.LpInteger, lowBound=0, upBound=1)
        for i in range(num_players)
    ]

    model += sum(decisions[i] * expected_points[i] for i in range(num_players)), "Objective"

    model += sum(decisions[i] * prices[i] for i in range(num_players)) <= 20000, "Budget"
    model += sum(decisions) == 10, "Team Size"

    model += sum(decisions[i] for i in range(num_players) if tours[i] == 'wta') == 5, "WTA"
    model += sum(decisions[i] for i in range(num_players) if tours[i] == 'atp') == 5, "ATP"

    model.solve(pulp.PULP_CBC_CMD(msg=False))

    return decisions
