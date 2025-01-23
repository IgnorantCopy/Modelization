import numpy as np
import pandas as pd

def get_weight(x):
    epsilon = 1e-6
    p = []
    ss = [np.sum(x[:, i]) for i in range(len(x[0]))]
    for row in x:
        temp = []
        for j, e in enumerate(row):
            temp.append(e / ss[j])
        p.append(temp)
    p = np.array(p)
    m = len(p)
    k = 1 / np.log(m)
    h = []
    for i in p.T:
        temp = 0
        for j in i:
            temp += j * np.log(j + epsilon)
        h.append(-k * temp)
    s = np.sum(h)
    n = len(h)
    w = [(1 - i) / (n - s) for i in h]
    return np.array(w)


def _get_time(data: pd.DataFrame) -> np.ndarray:
    time = data["elapsed_time"]
    x = []
    for i in time:
        hour, minute, second = i.split(':')
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        if hour >= 24:
            hour -= 24
        t = hour * 3600 + minute * 60 + second
        x.append(t)
    return np.array(x)


def _get_set_no(data: pd.DataFrame) -> np.ndarray:
    return data["set_no"].values


def _get_game_no(data: pd.DataFrame) -> list:
    game_no = data[["set_no", "game_no"]]
    set_num = game_no["set_no"].max()
    result = []
    for i in range(set_num):
        temp = game_no[game_no["set_no"] == i + 1]["game_no"].values
        result.append(temp)
    return result


def _get_point_no(data: pd.DataFrame) -> np.ndarray:
    return data["point_no"].values


def _get_p1_sets(data: pd.DataFrame) -> np.ndarray:
    return data["p1_sets"].values


def _get_p2_sets(data: pd.DataFrame) -> np.ndarray:
    return data["p2_sets"].values


def _get_p1_games(data: pd.DataFrame) -> np.ndarray:
    return data["p1_games"].values


def _get_p2_games(data: pd.DataFrame) -> np.ndarray:
    return data["p2_games"].values


def _get_p1_score(data: pd.DataFrame) -> np.ndarray:
    p1_score = data["p1_score"]
    p1_score = p1_score.replace('40', '45')
    p1_score = p1_score.replace('AD', '60')
    p1_score = p1_score.astype(int)
    return p1_score.values


def _get_p2_score(data: pd.DataFrame) -> np.ndarray:
    p2_score = data["p2_score"]
    p2_score = p2_score.replace('40', '45')
    p2_score = p2_score.replace('AD', '60')
    p2_score = p2_score.astype(int)
    return p2_score.values


def _get_score1(data: pd.DataFrame) -> np.ndarray:
    score1 = _get_p1_score(data) - _get_p2_score(data)
    for i, score in enumerate(score1):
        if abs(score) < 10:
            score *= 15
            score1[i] = score
    return score1


def _get_score2(data: pd.DataFrame) -> np.ndarray:
    return -_get_score1(data)


def _get_win_streak1(data: pd.DataFrame) -> np.ndarray:
    victor = _get_victor(data)
    win_streak = []
    count = 0
    for i in victor:
        if i == 1:
            count += 1
        elif i == 2:
            count = 0
        win_streak.append(count)
    return np.array(win_streak)


def _get_win_streak2(data: pd.DataFrame) -> np.ndarray:
    victor = _get_victor(data)
    win_streak = []
    count = 0
    for i in victor:
        if i == 1:
            count = 0
        elif i == 2:
            count += 1
        win_streak.append(count)
    return np.array(win_streak)


def _get_server1(data: pd.DataFrame) -> np.ndarray:
    return data["server"].replace(2, 0).values


def _get_server2(data: pd.DataFrame) -> np.ndarray:
    server2 = data["server"].values
    return (server2 - np.min(server2)) / (np.max(server2) - np.min(server2))


def _get_victor(data: pd.DataFrame) -> np.ndarray:
    return data["point_victor"].values


def _get_game_victor(data: pd.DataFrame) -> np.ndarray:
    return data.query("game_victor != 0")["game_victor"].values


def _get_set_victor(data: pd.DataFrame) -> np.ndarray:
    return data.query("set_victor != 0")["set_victor"].values


def _get_p1_break_pt_won(data: pd.DataFrame) -> np.ndarray:
    return data["p1_break_pt_won"].values


def _get_p2_break_pt_won(data: pd.DataFrame) -> np.ndarray:
    return data["p2_break_pt_won"].values


def _get_p1_break_pt_missed(data: pd.DataFrame) -> np.ndarray:
    return data["p1_break_pt_missed"].values


def _get_p2_break_pt_missed(data: pd.DataFrame) -> np.ndarray:
    return data["p2_break_pt_missed"].values


def _get_p1_distance_run(data: pd.DataFrame) -> np.ndarray:
    return data["p1_distance_run"].values


def _get_p2_distance_run(data: pd.DataFrame) -> np.ndarray:
    return data["p2_distance_run"].values


def _get_p1_distance_run_cum(data: pd.DataFrame) -> np.ndarray:
    return _get_p1_distance_run(data).cumsum()


def _get_p2_distance_run_cum(data: pd.DataFrame) -> np.ndarray:
    return _get_p2_distance_run(data).cumsum()


def _get_rally_count(data: pd.DataFrame) -> np.ndarray:
    return data["rally_count"].values


def _get_rally_count_cum(data: pd.DataFrame) -> np.ndarray:
    return _get_rally_count(data).cumsum()


def get_attributes(data: pd.DataFrame, *args):
    mapping = {
        "elapsed_time": _get_time(data),
        "set_no": _get_set_no(data),
        "game_no": _get_game_no(data),
        "point_no": _get_point_no(data),
        "p1_sets": _get_p1_sets(data),
        "p2_sets": _get_p2_sets(data),
        "p1_games": _get_p1_games(data),
        "p2_games": _get_p2_games(data),
        "p1_score": _get_p1_score(data),
        "p2_score": _get_p2_score(data),
        "score1": _get_score1(data),
        "score2": _get_score2(data),
        "win_streak1": _get_win_streak1(data),
        "win_streak2": _get_win_streak2(data),
        "server1": _get_server1(data),
        "server2": _get_server2(data),
        "victor": _get_victor(data),
        "game_victor": _get_game_victor(data),
        "set_victor": _get_set_victor(data),
        "p1_break_pt_won": _get_p1_break_pt_won(data),
        "p2_break_pt_won": _get_p2_break_pt_won(data),
        "p1_break_pt_missed": _get_p1_break_pt_missed(data),
        "p2_break_pt_missed": _get_p2_break_pt_missed(data),
        "p1_distance_run": _get_p1_distance_run(data),
        "p2_distance_run": _get_p2_distance_run(data),
        "p1_distance_run_cum": _get_p1_distance_run_cum(data),
        "p2_distance_run_cum": _get_p2_distance_run_cum(data),
        "rally_count": _get_rally_count(data),
        "rally_count_cum": _get_rally_count_cum(data),
    }
    return [mapping[arg] for arg in args]


def normalization(data: list, sgn: list):
    assert len(data) == len(sgn)
    for i, x in enumerate(data):
        if sgn[i]:
            data[i] = (x - np.min(x)) / (np.max(x) - np.min(x))
        else:
            data[i] = (np.max(x) - x) / (np.max(x) - np.min(x))
    return data
