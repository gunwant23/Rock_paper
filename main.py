from RPS_game import easy1, easy2, medium, medium2, markov_chain, human, random
import time
import os

# -------------------------
# Color & Emoji Helpers
# -------------------------
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

moves_emoji = {"R": "🪨 Rock", "P": "📄 Paper", "S": "✂️ Scissors"}

# -------------------------
# Clear screen function
# -------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# -------------------------
# USER Move Input
# -------------------------
def get_user_move():
    print(CYAN + "\nChoose your move:" + RESET)
    print(" 🪨  R - Rock\n 📄  P - Paper\n ✂️  S - Scissors")
    move = input("Your choice: ").strip().lower()

    if move in ["r", "rock"]:
        return "R"
    elif move in ["p", "paper"]:
        return "P"
    elif move in ["s", "scissor", "scissors"]:
        return "S"
    else:
        print(RED + "Invalid choice! Try again." + RESET)
        return get_user_move()


# -------------------------
# Human Player Wrapper
# -------------------------
def human_player(prev):
    return get_user_move()


# -------------------------
# Provided PLAY function
# -------------------------
def play(player1, player2, num_games, verbose=False):
    p1_prev = ""
    p2_prev = ""
    results = {"p1": 0, "p2": 0, "tie": 0}

    for _ in range(num_games):
        p1_play = player1(p2_prev)
        p2_play = player2(p1_prev)

        if p1_play == p2_play:
            results["tie"] += 1
            winner = YELLOW + "It's a Tie!" + RESET
        elif (p1_play == "P" and p2_play == "R") or \
             (p1_play == "R" and p2_play == "S") or \
             (p1_play == "S" and p2_play == "P"):
            results["p1"] += 1
            winner = GREEN + "You Win!" + RESET
        else:
            results["p2"] += 1
            winner = RED + "Bot Wins!" + RESET

        if verbose:
            print(f"\nYou: {moves_emoji[p1_play]}  |  Bot: {moves_emoji[p2_play]}")
            print(winner)

        p1_prev = p1_play
        p2_prev = p2_play
        time.sleep(0.6)

    return results


# -------------------------
# Choose Bot
# -------------------------
def select_bot():
    print(CYAN + "Select Difficulty Level:" + RESET)
    print("""
 1️⃣  Easy 1
 2️⃣  Easy 2
 3️⃣  Medium 1
 4️⃣  Medium 2
 5️⃣  Hard (Markov Chain)
 6️⃣  Random Bot
""")

    level = input("Enter choice (1–6): ").strip()

    bots = {
        "1": easy1,
        "2": easy2,
        "3": medium,
        "4": medium2,
        "5": markov_chain,
        "6": random
    }

    if level not in bots:
        print(RED + "Invalid option. Try again.\n" + RESET)
        return select_bot()

    print(GREEN + "\nBot Selected Successfully!\n" + RESET)
    return bots[level]


# -------------------------
# MAIN GAME
# -------------------------
def main():
    clear()
    print(YELLOW + "🎮 WELCOME TO ROCK • PAPER • SCISSORS 🎮" + RESET)
    time.sleep(1)

    while True:
        bot = select_bot()
        rounds = input("\nHow many rounds do you want to play? ").strip()

        if not rounds.isdigit():
            print(RED + "Enter a valid number!" + RESET)
            continue

        rounds = int(rounds)
        clear()

        print(CYAN + f"\nStarting Game for {rounds} Rounds...\n" + RESET)
        time.sleep(1)

        results = play(human_player, bot, rounds, verbose=True)

        print("\n" + YELLOW + "🏆 FINAL RESULTS 🏆" + RESET)
        print(f"😎 You Won: {GREEN}{results['p1']}{RESET}")
        print(f"🤖 Bot Won: {RED}{results['p2']}{RESET}")
        print(f"😐 Ties: {YELLOW}{results['tie']}{RESET}")

        again = input("\nPlay Again? (y/n): ").strip().lower()
        if again != "y":
            print(GREEN + "\nThanks for playing! 👋" + RESET)
            break
        clear()


if __name__ == "__main__":
    main()
