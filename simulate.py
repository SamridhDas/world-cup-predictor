import pandas as pd
import numpy as np
import random as random
df=pd.read_csv("data/team_stats.csv")
def simulate(team1,team2,knockout=False):
    extra_time = False
    penalties = False
    pen1=None
    pen2=None
    penalty_score = None

    t1 = df[df["Team"] == team1].iloc[0]
    t2 = df[df["Team"] == team2].iloc[0]



    attack1 = t1["Attack Rating"]
    defence1 = t1["Defence Rating"]

    attack2 = t2["Attack Rating"]
    defence2 = t2["Defence Rating"]

    strength1 = t1["Final Rating"]
    strength2 = t2["Final Rating"]

    strength_factor1 = strength1 / (strength1 + strength2)
    strength_factor2 = strength2 / (strength1 + strength2)

    base_xg1 = 2.8 * strength_factor1
    base_xg2 = 2.8 * strength_factor2

    attack_adjust1 = (attack1 / defence2)**0.3
    attack_adjust2 = (attack2 / defence1)**0.3

    xg1 = base_xg1 * attack_adjust1
    xg2 = base_xg2 * attack_adjust2

    elo_diff = (t1["Elo Rating"]-t2["Elo Rating"])


    elo_modifier = max(min(elo_diff/1000,0.20),-0.20)

    xg1 *= (1 + elo_modifier)
    xg2 *= (1 - elo_modifier)

    xg1=max(xg1,0.1)
    xg2=max(xg2,0.1)

    goals1=np.random.poisson(xg1)
    goals2=np.random.poisson(xg2)

    if goals1 > goals2:
        winner = team1

    elif goals2 > goals1:
        winner = team2

    else:
        winner = "Draw"
    
    shots1 = max(goals1 + 2, int(np.random.normal(xg1 * 7, 2)))
    shots2 = max(goals2 + 2, int(np.random.normal(xg2 * 7, 2)))

    shots_on_target1 = max(goals1, int(shots1 * np.random.uniform(0.3, 0.45)))
    shots_on_target2 = max(goals2, int(shots2 * np.random.uniform(0.3, 0.45)))

    total_attack = attack1+attack2
    pos1 = round((attack1 / total_attack) * 100)
    pos2 = 100 - pos1

    corners1 = max(1, int(shots1 / 3))
    corners2 = max(1, int(shots2 / 3))

    yellow1 = np.random.poisson(1.8)
    yellow2 = np.random.poisson(1.8)

    red1 = 1 if random.random() < 0.03 else 0
    red2 = 1 if random.random() < 0.03 else 0


    if knockout and winner == "Draw":

        extra_time = True

        extra_xg1 = xg1 / 3
        extra_xg2 = xg2 / 3

        extra_goals1 = np.random.poisson(extra_xg1)
        extra_goals2 = np.random.poisson(extra_xg2)

        goals1 += extra_goals1
        goals2 += extra_goals2

        extra_shots1 = max(extra_goals1, int(np.random.normal(extra_xg1 * 7, 1)))
        extra_shots2 = max(extra_goals2, int(np.random.normal(extra_xg2 * 7, 1)))

        shots1 += extra_shots1
        shots2 += extra_shots2

        shots_on_target1 += max(extra_goals1, int(extra_shots1 * 0.4))
        shots_on_target2 += max(extra_goals2, int(extra_shots2 * 0.4))

        corners1 += max(0, int(extra_shots1 / 3))
        corners2 += max(0, int(extra_shots2 / 3))

        yellow1 += np.random.poisson(0.5)
        yellow2 += np.random.poisson(0.5)

        if goals1 > goals2:
            winner = team1

        elif goals2 > goals1:
            winner = team2
        else:
            penalties = True
            elo1 = t1["Elo Rating"]
            elo2 = t2["Elo Rating"]

            pen_prob=0.5+((elo1-elo2)/2000)
            pen1 = 0
            pen2 = 0
            for _ in range(5):
                if random.random() < pen_prob:
                    pen1 += 1
                if random.random() < (1 - pen_prob):
                    pen2 += 1
            while pen1 == pen2:
                if random.random() < pen_prob:
                    pen1 += 1
                if random.random() < (1 - pen_prob):
                    pen2 += 1
            penalty_score = f"{pen1}-{pen2}"
            if pen1 > pen2:
                winner = team1
            else:
                winner = team2
            

                        

    return {
        "team1": team1,
        "team2": team2,

        "goals1": int(goals1),
        "goals2": int(goals2),

        "xg1": round(xg1, 2),
        "xg2": round(xg2, 2),

        "shots1": shots1,
        "shots2": shots2,

        "shots_on_target1": shots_on_target1,
        "shots_on_target2": shots_on_target2,

        "possession1": pos1,
        "possession2": pos2,

        "corners1": corners1,
        "corners2": corners2,

        "yellow1": yellow1,
        "yellow2": yellow2,

        "red1": red1,
        "red2": red2,

        "winner": winner,

        "extra_time": extra_time,
        "penalties": penalties,
        "penalty_score": penalty_score
    }



