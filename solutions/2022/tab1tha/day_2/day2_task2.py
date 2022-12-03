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

strategy = """A Y
B X
C Z"""

def find_winner(play_comb):
        #i_win = ["CX", "AY", "BZ"]
        i_win = ["CA", "AB", "BC"]
        same_play = ["AA", "BB", "CC"]
        if play_comb in i_win:
            winner = "me"
        elif play_comb in same_play:
            winner = "draw"
        else:
            winner = "not me"
        return winner

# creating play value
win_map = {"A":"B", "B":"C", "C":"A"}
draw_map = {"A":"A", "B":"B", "C":"C"}
lose_map = {"A":"C", "B":"A", "C":"B"}
strategy_map = {"X":lose_map, "Y":draw_map, "Z":win_map}
# calculating score
score_map = {"not me":0, "me":6, "draw":3}
play_map = {"A":1, "B":2, "C":3}


def planned_score(strategy):
    #  create columns
    rounds = [round.split(" ") for round in strategy.split("\n")]
    rounds_df = pd.DataFrame(rounds, columns=["not_me", "my_plan"])
    print(rounds_df)

    rounds_df_lose  = rounds_df[rounds_df["my_plan"]=="X"].copy()
    rounds_df_lose["me"] = rounds_df_lose["not_me"].map(lose_map)

    rounds_df_draw  = rounds_df[rounds_df["my_plan"]=="Y"].copy()
    rounds_df_draw["me"] = rounds_df_draw["not_me"].map(draw_map)

    rounds_df_win  = rounds_df[rounds_df["my_plan"]=="Z"].copy()
    rounds_df_win["me"] = rounds_df_win["not_me"].map(win_map)

    rounds_df = pd.concat([rounds_df_lose, rounds_df_draw, rounds_df_win], ignore_index=True)

    # # Find who the winner is
    rounds_df["round"] = rounds_df["not_me"] + rounds_df["me"]

    rounds_df["winner"] = rounds_df["round"].apply(find_winner)

    rounds_df["round_score"] = rounds_df["winner"].map(score_map)
    rounds_df["play_score"] = rounds_df["me"].map(play_map)
    rounds_df["score_per_round"] = rounds_df["round_score"] + rounds_df["play_score"]
    my_total_score = rounds_df["score_per_round"].sum()

    return my_total_score

result =  planned_score(play_plan)
print(result)