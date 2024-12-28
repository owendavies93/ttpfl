import cmd
import data
import sys

def main():
    print("Starting...")
    wta_file = sys.argv[1]
    atp_file = sys.argv[2]
    current_picks = []
    already_picked = []
    
    players, points, prices, tours = data.get_player_data(wta_file, atp_file)

    while True:
        print("Enter command: ", end="")
        current_picks, already_picked = cmd.execute_command(input().split(), players, points, prices, tours, current_picks, already_picked)


if __name__ == "__main__":
    main()
