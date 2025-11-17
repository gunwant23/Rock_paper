from RPS_game import easy1, easy2, medium, medium2, markov_chain, human, random
import time
import os

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

moves_ = {"R": "Rock", "P": "Paper", "S": "Scissors"}

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def get_user_move():
    print(CYAN + "\nChoose your move:" + RESET)
    print("  R - Rock\n  P - Paper\n  S - Scissors")

    move = input("Your choice: ").strip().lower()

    mapping = {
        "r": "R", "rock": "R",
        "p": "P", "paper": "P",
        "s": "S", "scissor": "S", "scissors": "S",
    }

    if move not in mapping:
        print(RED + "Invalid choice! Try again." + RESET)
        return get_user_move()

    return mapping[move]


def human_player(prev):
    return get_user_move()

# Result Computation

def winner_of(p1, p2):
    if p1 == p2:
        return "tie"

    wins = {
        ("P", "R"),
        ("R", "S"),
        ("S", "P"),
    }

    return "p1" if (p1, p2) in wins else "p2"

# PLAY Function

def play(player1, player2, num_games, names=("You", "Bot"), verbose=False):
    p1_prev = p2_prev = ""
    results = {"p1": 0, "p2": 0, "tie": 0}

    for _ in range(num_games):
        p1_play = player1(p2_prev)
        p2_play = player2(p1_prev)

        result = winner_of(p1_play, p2_play)
        results[result] += 1

        if verbose:
            print(f"\n{names[0]}: {moves_[p1_play]}  |  {names[1]}: {moves_emoji[p2_play]}")

            if result == "tie":
                print(YELLOW + "It's a Tie!" + RESET)
            elif result == "p1":
                print(GREEN + f"{names[0]} Wins!" + RESET)
            else:
                print(RED + f"{names[1]} Wins!" + RESET)

        p1_prev, p2_prev = p2_play, p1_play
        time.sleep(0.4)

    return results


# Bot Selection
def select_bot(prompt="Select Bot:"):
    print(CYAN + f"{prompt}" + RESET)
    print("""
 1. Easy 1
 2. Easy 2
 3. Medium 1
 4. Medium 2
 5. Hard (Markov Chain)
 6. Random Bot
""")

    bots = {
        "1": easy1,
        "2": easy2,
        "3": medium,
        "4": medium2,
        "5": markov_chain,
        "6": random
    }

    choice = input("Enter choice (1-6): ").strip()

    if choice not in bots:
        print(RED + "Invalid option. Try again.\n" + RESET)
        return select_bot(prompt)

    print(GREEN + "Bot Selected Successfully!\n" + RESET)
    return bots[choice], f"Bot-{choice}"

# -------------------------
def main():
    clear()
    print(YELLOW + "WELCOME TO ROCK • PAPER • SCISSORS" + RESET)
    time.sleep(1)

    while True:
        print(CYAN + "\nChoose Mode:" + RESET)
        print("""
 1. Human vs Bot
 2. Bot vs Bot
""")
        mode = input("Enter choice (1/2): ").strip()

        if mode not in ["1", "2"]:
            print(RED + "Invalid choice" + RESET)
            continue

        rounds = input("\nHow many rounds? ").strip()
        if not rounds.isdigit():
            print(RED + "Enter a valid number!" + RESET)
            continue

        rounds = int(rounds)
        clear()

        if mode == "1":
            bot, bot_name = select_bot()
            results = play(human_player, bot, rounds, names=("You", bot_name), verbose=True)

        else:  # BOT vs BOT
            bot1, name1 = select_bot("Select Bot 1:")
            bot2, name2 = select_bot("Select Bot 2:")

            print(CYAN + f"\n{YELLOW}{name1}{CYAN} VS {YELLOW}{name2}{RESET}")
            time.sleep(1)

            results = play(bot1, bot2, rounds, names=(name1, name2), verbose=True)

        # Final Results
        print("\n" + YELLOW + " FINAL RESULTS " + RESET)
        print(f"{GREEN}P1 Wins:{RESET} {results['p1']}")
        print(f"{RED}P2 Wins:{RESET} {results['p2']}")
        print(f"{YELLOW}Ties:{RESET} {results['tie']}")

        diff = results['p1'] - results['p2']
        if diff > 0:
            print(GREEN + f"Player 1 wins by {diff}!" + RESET)
        elif diff < 0:
            print(RED + f"Player 2 wins by {abs(diff)}!" + RESET)
        else:
            print(YELLOW + "It's a tie!" + RESET)

        again = input("\nPlay Again? (y/n): ").strip().lower()
        if again != "y":
            break

        clear()

    print(GREEN + "\nThanks for playing!" + RESET)


if __name__ == "__main__":
    main()
