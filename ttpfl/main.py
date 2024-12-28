import model
import data
import sys

def run_model(players, points, prices, tours, current_picks, already_picked):
    budget, decisions = model.run_model(points, prices, tours, current_picks, already_picked)

    selected_players = []
    team = []
    for i in range(len(decisions)):
        if decisions[i].value() == 1:
            if i in current_picks:
                team.append((players[i], points[i]))
            else:
                selected_players.append((players[i], points[i]))
    
    team.sort(key=lambda x: x[1], reverse=True)
    print("Picked players:")
    for player, points in team:
        print("{}: {}".format(player, points))

    print("\n")

    selected_players.sort(key=lambda x: x[1], reverse=True)
    print("Best remaining players:")
    for player, points in selected_players:
        print("{}: {}".format(player, points))

    print("\n")

    print("Budget remaining: {}".format(budget))

def execute_command(cmd, players, points, prices, tours, current_picks, already_picked):
    if cmd[0] == "run":
        run_model(players, points, prices, tours, current_picks, already_picked)
    elif cmd[0] == "pick":
        player = " ".join(cmd[1:])
        player_id = data.get_player_id(players, player)
        if player_id == -1:
            print("Player {} not found".format(player))
        else:
            budget = 20000
            for i in current_picks:
                budget -= prices[i]

            if budget < prices[player_id]:
                print("Not enough budget to pick {}".format(player))
            else:
                print("Picking {}".format(player))
                current_picks.append(player_id)
                print("Rerunning model...")
                run_model(players, points, prices, tours, current_picks, already_picked)

    elif cmd[0] == "rm":
        player = " ".join(cmd[1:])
        player_id = data.get_player_id(players, player)
        if player_id == -1:
            print("Player {} not found".format(player))
        else:
            print("Removing {}".format(player))
            already_picked.append(player_id)

        print("Rerunning model...")
        run_model(players, points, prices, tours, current_picks, already_picked)
    elif cmd[0] == "show":
        print("Current picks:")
        for i in current_picks:
            print(players[i])
    elif cmd[0] == "exit":
        print("Bye!")
        exit()

    return current_picks, already_picked

def main():
    print("Starting...")
    wta_file = sys.argv[1]
    atp_file = sys.argv[2]
    current_picks = []
    already_picked = []
    
    players, points, prices, tours = data.get_player_data(wta_file, atp_file)

    while True:
        print("Enter command: ", end="")
        current_picks, already_picked = execute_command(input().split(), players, points, prices, tours, current_picks, already_picked)


if __name__ == "__main__":
    main()
