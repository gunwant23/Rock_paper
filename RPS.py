def player(prev_play, opponent_history=[], my_history=[], play_order=[{}]):
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

    # --- Strategy 1: Quincy (fixed pattern) ---
    if opp_len >= 5:
        quincy_pattern = ["R", "P", "P", "S", "R"]
        matches = sum(opponent_history[-(i + 1)] == quincy_pattern[(opp_len - i - 1) % 5]
                      for i in range(min(20, opp_len)))
        if matches >= min(15, opp_len - 2):
            prediction = quincy_pattern[opp_len % 5]
            my_play = ideal_response[prediction]
            my_history.append(my_play)
            return my_play

    # --- Strategy 2: Kris (counters last move) ---
    if my_len >= 5:
        kris_matches = sum(opponent_history[-i] == ideal_response[my_history[-i - 1]]
                           for i in range(1, min(6, my_len)))
        if kris_matches >= 4:
            prediction = ideal_response[my_history[-1]]
            my_play = ideal_response[prediction]
            my_history.append(my_play)
            return my_play

    # --- Strategy 3: Mrugesh (counters my most frequent move) ---
    if my_len >= 10:
        last_10 = my_history[-10:]
        my_most = max(('R', 'P', 'S'), key=last_10.count)
        expected_mrugesh = ideal_response[my_most]

        if opp_len >= 10:
            opp_last_10 = opponent_history[-10:]
            opp_most = max(('R', 'P', 'S'), key=opp_last_10.count)
            if opp_most == expected_mrugesh and opp_last_10.count(expected_mrugesh) >= 5:
                prediction = my_most
                my_play = ideal_response[prediction]
                my_history.append(my_play)
                return my_play

    # --- Strategy 4: Abbey (tracks my 2-move patterns) ---
    if my_len >= 10:
        last_my = my_history[-1]
        pred_counts = {'R': 0, 'P': 0, 'S': 0}
        for i in range(2, my_len):
            if my_history[i - 1] == last_my:
                pred_counts[my_history[i]] += 1

        if sum(pred_counts.values()) >= 5:
            abbey_predict = max(pred_counts, key=pred_counts.get)
            abbey_expected = ideal_response[abbey_predict]

            abbey_matches = 0
            for i in range(1, min(6, my_len)):
                if my_len > i + 1:
                    prev_my = my_history[-(i + 1)]
                    pred_map = {'R': 0, 'P': 0, 'S': 0}
                    for j in range(2, my_len - i):
                        if my_history[j - 1] == prev_my:
                            pred_map[my_history[j]] += 1
                    if sum(pred_map.values()) > 0:
                        abbey_would_play = ideal_response[max(pred_map, key=pred_map.get)]
                        if opponent_history[-i] == abbey_would_play:
                            abbey_matches += 1

            if abbey_matches >= 3:
                prediction = abbey_expected
                my_play = ideal_response[prediction]
                my_history.append(my_play)
                return my_play

    # --- General Markov Chain Prediction ---
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
