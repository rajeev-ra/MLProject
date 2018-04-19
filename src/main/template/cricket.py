import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os.path

class Cricket(object):
    ball_by_ball = []
    match = []
    player = []
    player_match = []
    season = []
    team = []

    def __init__(self):
        self.ball_by_ball = pd.read_csv("./../../../data/cricket/raw/Ball_by_Ball.csv")
        self.match = pd.read_csv("./../../../data/cricket/raw/match.csv")
        self.player = pd.read_csv("./../../../data/cricket/raw/player.csv")
        self.player_match = pd.read_csv("./../../../data/cricket/raw/player_match.csv")
        self.season = pd.read_csv("./../../../data/cricket/raw/season.csv")
        self.team = pd.read_csv("./../../../data/cricket/raw/team.csv")


    def PlayerData(self, player_id, property = "Player_Name"):
        try:
            return self.player[self.player["Player_Id"] == player_id][property].values[0]
        except:
            return None

    def TeamName(self, team_id, short = False):
        p = "Team_Short_Code" if short else "Team_Name"
        try:
            return self.team[self.team["Team_Id"] == team_id][p].values[0]
        except:
            return None

    def Captains(self, match = 0, team_name = False, team_name_short = False, player_name = False):
        #print(self.player_match)
        a = self.player_match[self.player_match["Is_Captain"] == 1]
        if match == 0:
            return a[["Team_Id", "Player_Id"]]
        else:
            return a[a["Match_Id"] == match][["Team_Id", "Player_Id"]]
