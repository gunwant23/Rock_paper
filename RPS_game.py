# DO NOT MODIFY THIS FILE

import random


def play(player1, player2, num_games, verbose=False):
    p1_prev_play = ""
    p2_prev_play = ""
    results = {"p1": 0, "p2": 0, "tie": 0}

    for _ in range(num_games):
        p1_play = player1(p2_prev_play)
        p2_play = player2(p1_prev_play)

        if p1_play == p2_play:
            results["tie"] += 1
            winner = "Tie."
        elif (p1_play == "P" and p2_play == "R") or (
                p1_play == "R" and p2_play == "S") or (p1_play == "S"
                                                       and p2_play == "P"):
            results["p1"] += 1
            winner = "Player 1 wins."
        elif p2_play == "P" and p1_play == "R" or p2_play == "R" and p1_play == "S" or p2_play == "S" and p1_play == "P":
            results["p2"] += 1
            winner = "Player 2 wins."

        if verbose:
            print("Player 1:", p1_play, "| Player 2:", p2_play)
            print(winner)
            print()

        p1_prev_play = p1_play
        p2_prev_play = p2_play

    games_won = results['p2'] + results['p1']

    if games_won == 0:
        win_rate = 0
    else:
        win_rate = results['p1'] / games_won * 100

    print("Final results:", results)
    print(f"Player 1 win rate: {win_rate}%")

    return (win_rate)


def easy1(prev_play, counter=[0]):

    counter[0] += 1
    choices = ["R", "R", "P", "P", "S"]
    return choices[counter[0] % len(choices)]


def easy2(prev_opponent_play, opponent_history=[]):
    opponent_history.append(prev_opponent_play)
    last_ten = opponent_history[-10:]
    most_frequent = max(set(last_ten), key=last_ten.count)

    if most_frequent == '':
        most_frequent = "S"

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[most_frequent]


def medium(prev_opponent_play):
    if prev_opponent_play == '':
        prev_opponent_play = "R"
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prev_opponent_play]


def medium2(prev_opponent_play,
          opponent_history=[],
          play_order=[{
              "RR": 0,
              "RP": 0,
              "RS": 0,
              "PR": 0,
              "PP": 0,
              "PS": 0,
              "SR": 0,
              "SP": 0,
              "SS": 0,
          }]):

    if not prev_opponent_play:
        prev_opponent_play = 'R'
    opponent_history.append(prev_opponent_play)

    last_two = "".join(opponent_history[-2:])
    if len(last_two) == 2:
        play_order[0][last_two] += 1

    potential_plays = [
        prev_opponent_play + "R",
        prev_opponent_play + "P",
        prev_opponent_play + "S",
    ]

    sub_order = {
        k: play_order[0][k]
        for k in potential_plays if k in play_order[0]
    }

    prediction = max(sub_order, key=sub_order.get)[-1:]

    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[prediction]


def human(prev_opponent_play):
    play = ""
    while play not in ['R', 'P', 'S']:
        play = input("[R]ock, [P]aper, [S]cissors? ")
        print(play)
    return play


def random_bot(prev_opponent_play):
    return random.choice(['R', 'P', 'S'])

def markov_chain(prev_play, opponent_history=[], my_history=[], play_order=[{}]):
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}

    # Reset for new game
    if not prev_play:
        opponent_history.clear()
        my_history.clear()
        play_order.clear()
        play_order.append({})
        return 'R'

    opponent_history.append(prev_play)
    records = play_order[0]

    # Update opponent-only Markov chain
    opp_len = len(opponent_history)
    for i in range(1, min(6, opp_len)):
        pattern = "".join(opponent_history[-i-1:-1])
        rec = records.setdefault(pattern, {'R': 0, 'P': 0, 'S': 0})
        rec[prev_play] += 1

    # Update combined pattern chain
    my_len = len(my_history)
    for i in range(1, min(3, my_len + 1)):
        if opp_len > i:
            combined = "".join(my_history[-i:]) + "|" + "".join(opponent_history[-i-1:-1])
            rec = records.setdefault(combined, {'R': 0, 'P': 0, 'S': 0})
            rec[prev_play] += 1

    prediction = 'R'             
    best_prediction, best_confidence = None, 0
    for length in range(min(5, opp_len), 0, -1):
        pattern = "".join(opponent_history[-length:])
        if pattern in records:
            counts = records[pattern]
            total = sum(counts.values())
            if total:
                pred = max(counts, key=counts.get)
                confidence = counts[pred] / total
                if confidence > best_confidence:
                    best_confidence, best_prediction = confidence, pred

    if best_prediction:
        prediction = best_prediction
    elif opp_len >= 3:
        recent = opponent_history[-5:]
        prediction = max(('R', 'P', 'S'), key=recent.count)

    my_play = ideal_response[prediction]
    my_history.append(my_play)
    return my_play