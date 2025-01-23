import random
import numpy as np


server = random.randint(1, 2)


def simulate_point(p):
    return 1 if random.random() < p else 2


def simulate_game(p: float, victor: list, server1: list, server2: list, p1_score: list, p2_score: list):
    global server
    score1 = 0
    score2 = 0
    while abs(score1 - score2) < 2:
        if server == 1:
            server1.append(1)
            server2.append(0)
            victor.append(1)
        else:
            server1.append(0)
            server2.append(1)
            victor.append(2)
        if simulate_point(p) == 1:
            score1 += 1

        else:
            score2 += 1
        p1_score.append(score1 * 15)
        p2_score.append(score2 * 15)
    server = server % 2 + 1
    return score1 > score2


def simulate_set(p, victor, server1, server2, p1_score, p2_score):
    score1 = 0
    score2 = 0
    while not is_finished(score1, score2):
        if simulate_game(p, victor, server1, server2, p1_score, p2_score):
            score1 += 1
        else:
            score2 += 1
    return score1 > score2


def simulate_match(p, victor, server1, server2, p1_score, p2_score):
    score1 = 0
    score2 = 0
    while score1 != 3 and score2 != 3:
        if simulate_set(p, victor, server1, server2, p1_score, p2_score):
            score1 += 1
        else:
            score2 += 1
    return score1 > score2


def is_finished(score1, score2):
    if abs(score1 - score2) == 2 and (score1 == 6 or score2 == 6):
        return True
    if score1 == 7 or score2 == 7:
        return True
    return False


def simulate(p):
    victor = []
    server1 = []
    server2 = []
    p1_score = []
    p2_score = []
    simulate_match(p, victor, server1, server2, p1_score, p2_score)

    p1_score = np.array(p1_score)
    p2_score = np.array(p2_score)
    score1 = p1_score - p2_score
    score2 = -score1
    score1 = (score1 - np.min(score1)) / (np.max(score1) - np.min(score1))
    score2 = (score2 - np.min(score2)) / (np.max(score2) - np.min(score2))

    continue_score1 = []
    continue_score2 = []
    continue1 = 0
    continue2 = 0
    for i in victor:
        if i == 1:
            continue1 += 1
            continue2 = 0
        elif i == 2:
            continue2 += 1
            continue1 = 0
        continue_score1.append(continue1)
        continue_score2.append(continue2)
    continue_score1 = np.array(continue_score1)
    continue_score2 = np.array(continue_score2)
    continue_score1 = (continue_score1 - np.min(continue_score1)) / (np.max(continue_score1) - np.min(continue_score1))
    continue_score2 = (continue_score2 - np.min(continue_score2)) / (np.max(continue_score2) - np.min(continue_score2))

    return server1, server2, score1, score2, continue_score1, continue_score2