import csv
import os

state_file = "/tmp/ttpfl.state"

def get_player_id(players, player):
    for i in range(len(players)):
        if players[i] == player:
            return i
    return -1

def save_state(current_picks, already_picked):
    with open(state_file, "w") as f:
        f.write(" ".join(str(i) for i in current_picks) + "\n")
        f.write(" ".join(str(i) for i in already_picked) + "\n")

def load_state():
    if not os.path.exists(state_file):
        return [], []

    with open(state_file, "r") as f:
        current_picks = [int(i) for i in f.readline().split()]
        already_picked = [int(i) for i in f.readline().split()]
        return current_picks, already_picked

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
