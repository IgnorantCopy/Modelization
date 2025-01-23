import pandas as pd
import numpy as np
from utils import get_attributes, normalization
from models import momentum_model


data = pd.read_csv("./data/Wimbledon_featured_matches.csv")
player1 = data["player1"].value_counts()
player2 = data["player2"].value_counts()
player_names = list(player1.index) + list(player2.index)
player_names = list(set(player_names))
input_data = []
for name in player_names:
    df1 = data.query("player1 == @name")
    df2 = data.query("player2 == @name")
    if len(df1) != 0:
        server1, server2, score1, score2, win_streak1, win_streak2, distance1, distance2, break_won1, break_won2, break_missed1, break_missed2 = (
        get_attributes(df1, "server1", "server2", "score1", "score2", "win_streak1", "win_streak2", "p1_distance_run_cum", "p2_distance_run_cum",
                       "p1_break_pt_won", "p2_break_pt_won", "p1_break_pt_missed", "p2_break_pt_missed"))
        score1, score2, win_streak1, win_streak2, distance1, distance2 = (
            normalization([score1, score2, win_streak1, win_streak2, distance1, distance2],
                          [1, 1, 1, 1, 0, 0]))
        x1 = [server1, score1, win_streak1, distance1, break_won1, break_missed1]
        x2 = [server2, score2, win_streak2, distance2, break_won2, break_missed2]
        if len(np.unique(break_won1)) == 1 or len(np.unique(break_won2)) == 1:
            print(name, "has no break point won data")
            x1.pop(-2)
            x2.pop(-2)
        if len(np.unique(break_missed1)) == 1 or len(np.unique(break_missed2)) == 1:
            print(name, "has no break point missed data")
            x1.pop(-1)
            x2.pop(-1)
        y1, y2 = momentum_model(x1, x2)
        for i in range(len(y1)):
            input_data.append({
                "name": name,
                "score": score1[i],
                "break_pt_won": break_won1[i],
                "break_pt_missed": break_missed1[i],
                "momentum": y1[i]
            })
    if len(df2) != 0:
        server1, server2, score1, score2, win_streak1, win_streak2, distance1, distance2, break_won1, break_won2, break_missed1, break_missed2 = (
        get_attributes(df2, "server1", "server2", "score1", "score2", "win_streak1", "win_streak2", "p1_distance_run_cum", "p2_distance_run_cum",
                       "p1_break_pt_won", "p2_break_pt_won", "p1_break_pt_missed", "p2_break_pt_missed"))
        score1, score2, win_streak1, win_streak2, distance1, distance2 = (
            normalization([score1, score2, win_streak1, win_streak2, distance1, distance2],
                          [1, 1, 1, 1, 0, 0]))
        x1 = [server1, score1, win_streak1, distance1, break_won1, break_missed1]
        x2 = [server2, score2, win_streak2, distance2, break_won2, break_missed2]
        if len(np.unique(break_won1)) == 1 or len(np.unique(break_won2)) == 1:
            print(name, "has no break point won data")
            x1.pop(-2)
            x2.pop(-2)
        if len(np.unique(break_missed1)) == 1 or len(np.unique(break_missed2)) == 1:
            print(name, "has no break point missed data")
            x1.pop(-1)
            x2.pop(-1)
        y1, y2 = momentum_model(x1, x2)
        for i in range(len(y2)):
            input_data.append({
                "name": name,
                "score": score1[i],
                "break_pt_won": break_won1[i],
                "break_pt_missed": break_missed1[i],
                "momentum": y2[i]
            })