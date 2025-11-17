import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import random as rand
from RPS_game import easy1, easy2, medium, medium2, markov_chain

def random_bot(prev_play):
    return rand.choice(['R', 'P', 'S'])

bots = {
    "Easy 1": easy1,
    "Easy 2": easy2,
    "Medium 1": medium,
    "Medium 2": medium2,
    "Hard (Markov Chain)": markov_chain,
    "Random Bot": random_bot
}

def winner_of(p1, p2):
    if p1 == p2:
        return "tie"
    wins = {("P", "R"), ("R", "S"), ("S", "P")}
    return "p1" if (p1, p2) in wins else "p2"

def play_games(player1, player2, num_games):
    p1_prev = p2_prev = ""
    results = {"p1": 0, "p2": 0, "tie": 0}
    history = []

    for _ in range(num_games):
        p1_play = player1(p2_prev)
        p2_play = player2(p1_prev)

        result = winner_of(p1_play, p2_play)
        results[result] += 1
        history.append(result)

        p1_prev, p2_prev = p2_play, p1_play

    return results, history


def plot_graph(history, name1, name2):
    p1 = p2 = 0
    win_p1, win_p2 = [], []

    for i, h in enumerate(history):
        if h == "p1": p1 += 1
        elif h == "p2": p2 += 1
        total = i + 1
        win_p1.append(100*p1/total)
        win_p2.append(100*p2/total)

    plt.figure(figsize=(7,5))
    plt.plot(win_p1, label=name1)
    plt.plot(win_p2, label=name2)
    plt.xlabel("Rounds")
    plt.ylabel("Win %")
    plt.title("Win Rate Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()



def start_gui():
    root = tk.Tk()
    root.title("Rock Paper Scissors – Bot vs Bot GUI")
    root.geometry("500x400")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12))
    style.configure("TLabel", font=("Arial", 12))

    bot1_var = tk.StringVar()
    bot2_var = tk.StringVar()
    round_var = tk.StringVar(value="50")

    ttk.Label(root, text="Select Bot 1:").pack(pady=10)
    bot1_box = ttk.Combobox(root, textvariable=bot1_var, values=list(bots.keys()))
    bot1_box.current(0)
    bot1_box.pack()

    ttk.Label(root, text="Select Bot 2:").pack(pady=10)
    bot2_box = ttk.Combobox(root, textvariable=bot2_var, values=list(bots.keys()))
    bot2_box.current(1)
    bot2_box.pack()

    ttk.Label(root, text="Number of Rounds:").pack(pady=10)
    ttk.Entry(root, textvariable=round_var).pack()

    def run_match():
        name1, name2 = bot1_var.get(), bot2_var.get()

        if name1 == name2:
            messagebox.showerror("Error", "Please select 2 different bots.")
            return

        try:
            rounds = int(round_var.get())
        except:
            messagebox.showerror("Error", "Invalid round number.")
            return

        bot1 = bots[name1]
        bot2 = bots[name2]

        results, history = play_games(bot1, bot2, rounds)

        messagebox.showinfo("Results", f"{name1} Wins: {results['p1']}\n{name2} Wins: {results['p2']}\nTies: {results['tie']}")
        plot_graph(history, name1, name2)

    ttk.Button(root, text="Run Match", command=run_match).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
