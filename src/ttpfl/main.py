import ttpfl.cmd as cmd
import ttpfl.data as data
import sys

def main():
    print("Starting...")
    wta_file = sys.argv[1]
    atp_file = sys.argv[2]
    injury_list_file = sys.argv[3]

    current_picks, already_picked = data.load_state()
    
    players, points, prices, tours = data.get_player_data(wta_file, atp_file)

    injury_list = data.get_injury_list(injury_list_file, players)

    while True:
        print("Enter command: ", end="")
        current_picks, already_picked = cmd.execute_command(players, points, prices, tours, current_picks, already_picked, injury_list)


if __name__ == "__main__":
    main()
