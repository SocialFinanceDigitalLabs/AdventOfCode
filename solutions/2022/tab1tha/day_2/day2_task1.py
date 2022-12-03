"""
Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. 
If both players choose the same shape, the round instead ends in a draw.
A for Rock, B for Paper, and C for Scissors
X for Rock, Y for Paper, and Z for Scissors
1 for Rock, 2 for Paper, and 3 for Scissors
0 if you lost, 3 if the round was a draw, and 6 if you won
"""

import pandas as pd

from input_day2 import play_plan

def find_winner(play_comb):
        i_win = ["CX", "AY", "BZ"]
        same_play = ["AX", "BY", "CZ"]
        if play_comb in i_win:
            winner = "me"
        elif play_comb in same_play:
            winner = "draw"
        else:
            winner = "not me"
        return winner

score_map = {"not me":0, "me":6, "draw":3}
play_map = {"X":1, "Y":2, "Z":3}

def strategy_score(strategy):
    rounds = [round.split(" ") for round in strategy.split("\n")]
    rounds_df = pd.DataFrame(rounds, columns=["not_me", "me"])
    rounds_df["round"] = rounds_df["not_me"] + rounds_df["me"]
    
    rounds_df["winner"] = rounds_df["round"].apply(find_winner)

    rounds_df["round_score"] = rounds_df["winner"].map(score_map)
    rounds_df["play_score"] = rounds_df["me"].map(play_map)
    rounds_df["score_per_round"] = rounds_df["round_score"] + rounds_df["play_score"]
    my_total_score = rounds_df["score_per_round"].sum()
    
    return my_total_score

result =  strategy_score(play_plan)
print(result)