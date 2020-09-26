
def take_input():
    print("Please enter the mode of the game: 2,3,4")
    mode = input()
    players = []

    if int(mode) == 2:
        player_1 = input("Enter the name of player1: ")
        player_2 = input("Enter the name of player2: ")
        players.append(player_1)
        players.append(player_2)

    elif int(mode) == 3:
        player_1 = input("Enter the name of player1: ")
        player_2 = input("Enter the name of player2: ")
        player_3 = input("Enter the name of player3: ")
        players.append(player_1)
        players.append(player_2)
        players.append(player_3)

    elif int(mode) == 4:
        player_1 = input("Enter the name of player1: ")
        player_2 = input("Enter the name of player2: ")
        player_3 = input("Enter the name of player3: ")
        player_4 = input("Enter the name of player4: ")
        players.append(player_1)
        players.append(player_2)
        players.append(player_3)
        players.append(player_4)

    return mode,players
