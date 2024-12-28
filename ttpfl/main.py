import model
import sys

def run_model(wta_file, atp_file, current_picks, already_picked):
    players, points, prices, tours = model.get_player_data(wta_file, atp_file)
    decisions = model.run_model(points, prices, tours)

    for i in range(len(decisions)):
        if decisions[i].value() == 1:
            print(players[i], points[i], prices[i], tours[i])

def execute_command(cmd, wta_file, atp_file, current_picks, already_picked):
    if cmd[0] == "run":
        run_model(wta_file, atp_file, current_picks, already_picked)
    elif cmd[0] == "pick":
        print("TODO")
    elif cmd[0] == "unpick":
        print("TODO")
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

    while True:
        print("Enter command: ", end="")
        current_picks, already_picked = execute_command(input().split(), wta_file, atp_file, current_picks, already_picked)


if __name__ == "__main__":
    main()
