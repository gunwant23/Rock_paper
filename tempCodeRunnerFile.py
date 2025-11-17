def play(player1, player2, num_games, names=("You", "Bot"), verbose=False):
    p1_prev = p2_prev = ""
    results = {"p1": 0, "p2": 0, "tie": 0}
    history = []
    
    for _ in range(num_games):
        p1_play = player1(p1_prev)
        p2_play = player2(p2_prev)

        result = winner_of(p1_play, p2_play)
        results[result] += 1
        history.append(result)

        if verbose:
            print(f"\nRound {_ + 1}:")
            print(f"{names[0]}: {moves_[p1_play]}  |  {names[1]}: {moves_[p2_play]}")

            if result == "tie":
                print(YELLOW + "It's a Tie!" + RESET)
            elif result == "p1":
                print(GREEN + f"{names[0]} Wins!" + RESET)
            else:
                print(RED + f"{names[1]} Wins!" + RESET)
        
        p1_prev, p2_prev = p2_play, p1_play
        time.sleep(0.4)
