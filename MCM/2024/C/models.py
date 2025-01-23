import numpy as np
from utils import get_weight


def momentum_model(player1: list, player2: list):
    x1 = np.vstack(player1).T
    w1 = get_weight(x1)
    print(w1)
    x2 = np.vstack(player2).T
    w2 = get_weight(x2)
    print(w2)
    y1 = (x1 @ w1.T).T
    y2 = (x2 @ w2.T).T
    return y1, y2