import simulate as simulate
import pandas as pd

groups = {
    "A": ["Mexico", "South Africa", "South Korea", "Czechia"],
    "B": ["Canada", "Bosnia and Herzegovina", "Qatar", "Switzerland"],
    "C": ["Brazil", "Morocco", "Haiti", "Scotland"],
    "D": ["United States", "Paraguay", "Australia", "Turkey"],
    "E": ["Germany", "Curacao", "Ivory Coast", "Ecuador"],
    "F": ["Netherlands", "Japan", "Sweden", "Tunisia"],
    "G": ["Belgium", "Egypt", "Iran", "New Zealand"],
    "H": ["Spain", "Cape Verde", "Saudi Arabia", "Uruguay"],
    "I": ["France", "Senegal", "Iraq", "Norway"],
    "J": ["Argentina", "Algeria", "Austria", "Jordan"],
    "K": ["Portugal", "DR Congo", "Uzbekistan", "Colombia"],
    "L": ["England", "Croatia", "Ghana", "Panama"]
}

TEAM_INFO = {
    "Mexico": {"code": "MEX", "logo": "/logos/mexico.png"},
    "South Africa": {"code": "RSA", "logo": "/logos/south_africa.png"},
    "South Korea": {"code": "KOR", "logo": "/logos/south_korea.png"},
    "Czechia": {"code": "CZE", "logo": "/logos/czechia.png"},
    "Canada": {"code": "CAN", "logo": "/logos/canada.png"},
    "Bosnia and Herzegovina": {"code": "BIH", "logo": "/logos/bosnia.png"},
    "Qatar": {"code": "QAT", "logo": "/logos/qatar.png"},
    "Switzerland": {"code": "SUI", "logo": "/logos/switzerland.png"},
    "Brazil": {"code": "BRA", "logo": "/logos/brazil.png"},
    "Morocco": {"code": "MAR", "logo": "/logos/morocco.png"},
    "Haiti": {"code": "HAI", "logo": "/logos/haiti.png"},
    "Scotland": {"code": "SCO", "logo": "/logos/scotland.png"},
    "United States": {"code": "USA", "logo": "/logos/usa.png"},
    "Paraguay": {"code": "PAR", "logo": "/logos/paraguay.png"},
    "Australia": {"code": "AUS", "logo": "/logos/australia.png"},
    "Turkey": {"code": "TUR", "logo": "/logos/turkey.png"},
    "Germany": {"code": "GER", "logo": "/logos/germany.png"},
    "Curacao": {"code": "CUW", "logo": "/logos/curacao.png"},
    "Ivory Coast": {"code": "CIV", "logo": "/logos/ivory_coast.png"},
    "Ecuador": {"code": "ECU", "logo": "/logos/ecuador.png"},
    "Netherlands": {"code": "NED", "logo": "/logos/netherlands.png"},
    "Japan": {"code": "JPN", "logo": "/logos/japan.png"},
    "Sweden": {"code": "SWE", "logo": "/logos/sweden.png"},
    "Tunisia": {"code": "TUN", "logo": "/logos/tunisia.png"},
    "Belgium": {"code": "BEL", "logo": "/logos/belgium.png"},
    "Egypt": {"code": "EGY", "logo": "/logos/egypt.png"},
    "Iran": {"code": "IRN", "logo": "/logos/iran.png"},
    "New Zealand": {"code": "NZL", "logo": "/logos/new_zealand.png"},
    "Spain": {"code": "ESP", "logo": "/logos/spain.png"},
    "Cape Verde": {"code": "CPV", "logo": "/logos/cape_verde.png"},
    "Saudi Arabia": {"code": "KSA", "logo": "/logos/saudi_arabia.png"},
    "Uruguay": {"code": "URU", "logo": "/logos/uruguay.png"},
    "France": {"code": "FRA", "logo": "/logos/france.png"},
    "Senegal": {"code": "SEN", "logo": "/logos/senegal.png"},
    "Iraq": {"code": "IRQ", "logo": "/logos/iraq.png"},
    "Norway": {"code": "NOR", "logo": "/logos/norway.png"},
    "Argentina": {"code": "ARG", "logo": "/logos/argentina.png"},
    "Algeria": {"code": "ALG", "logo": "/logos/algeria.png"},
    "Austria": {"code": "AUT", "logo": "/logos/austria.png"},
    "Jordan": {"code": "JOR", "logo": "/logos/jordan.png"},
    "Portugal": {"code": "POR", "logo": "/logos/portugal.png"},
    "DR Congo": {"code": "COD", "logo": "/logos/dr_congo.png"},
    "Uzbekistan": {"code": "UZB", "logo": "/logos/uzbekistan.png"},
    "Colombia": {"code": "COL", "logo": "/logos/colombia.png"},
    "England": {"code": "ENG", "logo": "/logos/england.png"},
    "Croatia": {"code": "CRO", "logo": "/logos/croatia.png"},
    "Ghana": {"code": "GHA", "logo": "/logos/ghana.png"},
    "Panama": {"code": "PAN", "logo": "/logos/panama.png"}
}

FIXED_RU_MATCHUPS = [
    ("A", "B"),
    ("E", "I"),
    ("K", "L"),
    ("D", "G"),
]

FIXED_W_RU_MATCHUPS = [
    ("F", "C"),
    ("C", "F"),
    ("H", "J"),
    ("J", "H"),
]

WINNER_VS_3RD_ELIGIBLE = {
    "E": {"A", "B", "C", "D", "F"},
    "I": {"C", "D", "F", "G", "H"},
    "A": {"C", "E", "F", "H", "I"},
    "L": {"E", "H", "I", "J", "K"},
    "D": {"B", "E", "F", "I", "J"},
    "G": {"A", "E", "H", "I", "J"},
    "B": {"E", "F", "G", "I", "J"},
    "K": {"D", "E", "I", "J", "L"},
}


def assign_third_place_teams(best_third_dict):
    unassigned_thirds = dict(best_third_dict)
    assignment = {}
    for slot in sorted(
        WINNER_VS_3RD_ELIGIBLE.keys(),
        key=lambda s: len(WINNER_VS_3RD_ELIGIBLE[s] & set(unassigned_thirds.keys()))
    ):
        eligible = WINNER_VS_3RD_ELIGIBLE[slot] & set(unassigned_thirds.keys())
        if not eligible:
            eligible = set(unassigned_thirds.keys())
        chosen_group = next(iter(eligible))
        assignment[slot] = unassigned_thirds.pop(chosen_group)
    return assignment


def simulate_group(teams, group_name):
    fixtures = []
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            fixtures.append((teams[i], teams[j]))
    table = {}
    for team in teams:
        table[team] = {
            "Points": 0,
            "Wins": 0,
            "Draws": 0,
            "Losses": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "FairPlay": 0
        }
    match_results = []
    for team1, team2 in fixtures:
        result = simulate.simulate(team1, team2)
        result["stage"] = f"Group {group_name}"
        result["team1_code"] = TEAM_INFO[result["team1"]]["code"]
        result["team2_code"] = TEAM_INFO[result["team2"]]["code"]
        result["team1_logo"] = TEAM_INFO[result["team1"]]["logo"]
        result["team2_logo"] = TEAM_INFO[result["team2"]]["logo"]
        result["scoreline"] = (
            f"{result['team1']} "
            f"{result['goals1']}-{result['goals2']} "
            f"{result['team2']}"
        )
        goals1 = result["goals1"]
        goals2 = result["goals2"]
        table[team1]["GF"] += goals1
        table[team1]["GA"] += goals2
        table[team2]["GF"] += goals2
        table[team2]["GA"] += goals1
        if goals1 > goals2:
            table[team1]["Points"] += 3
            table[team1]["Wins"] += 1
            table[team2]["Losses"] += 1
        elif goals2 > goals1:
            table[team2]["Points"] += 3
            table[team2]["Wins"] += 1
            table[team1]["Losses"] += 1
        else:
            table[team1]["Points"] += 1
            table[team2]["Points"] += 1
            table[team1]["Draws"] += 1
            table[team2]["Draws"] += 1
        table[team1]["FairPlay"] += (result["yellow1"] * -1 + result["red1"] * -4)
        table[team2]["FairPlay"] += (result["yellow2"] * -1 + result["red2"] * -4)
        match_results.append(result)
    for team in table:
        table[team]["GD"] = table[team]["GF"] - table[team]["GA"]
    group_df = pd.DataFrame(table).T
    group_df = group_df.sort_values(
        by=["Points", "GD", "GF", "FairPlay"],
        ascending=False
    )
    return {
        "table": group_df,
        "results": match_results,
        "first": group_df.index[0],
        "second": group_df.index[1],
        "third": group_df.index[2],
        "third_stats": group_df.iloc[2].to_dict()
    }


def play_rounds(teams, match_history, stage):
    winners = []
    for i in range(0, len(teams), 2):
        result = simulate.simulate(teams[i], teams[i + 1], knockout=True)
        result["stage"] = stage
        result["match_id"] = len(match_history) + 1
        result["team1_code"] = TEAM_INFO[result["team1"]]["code"]
        result["team2_code"] = TEAM_INFO[result["team2"]]["code"]
        result["team1_logo"] = TEAM_INFO[result["team1"]]["logo"]
        result["team2_logo"] = TEAM_INFO[result["team2"]]["logo"]
        result["scoreline"] = (
            f"{result['team1']} "
            f"{result['goals1']}-{result['goals2']} "
            f"{result['team2']}"
        )
        match_history.append(result)
        winners.append(result["winner"])
    return winners


def play_matchups(matchups, match_history, stage):
    winners = []
    for team1, team2 in matchups:
        result = simulate.simulate(team1, team2, knockout=True)
        result["stage"] = stage
        result["match_id"] = len(match_history) + 1
        result["team1_code"] = TEAM_INFO[result["team1"]]["code"]
        result["team2_code"] = TEAM_INFO[result["team2"]]["code"]
        result["team1_logo"] = TEAM_INFO[result["team1"]]["logo"]
        result["team2_logo"] = TEAM_INFO[result["team2"]]["logo"]
        result["scoreline"] = (
            f"{result['team1']} "
            f"{result['goals1']}-{result['goals2']} "
            f"{result['team2']}"
        )
        match_history.append(result)
        winners.append(result["winner"])
    return winners


def simulate_world_cup(groups, verbose=False):
    match_history = []
    group_winners = {}
    group_runners = {}
    third_place_table = []

    for group_name, teams in groups.items():
        result = simulate_group(teams, group_name)
        for match in result["results"]:
            match["match_id"] = len(match_history) + 1
            match_history.append(match)
        if verbose:
            print(f"\nGROUP {group_name}")
            print(result["table"])
        group_winners[group_name] = result["first"]
        group_runners[group_name] = result["second"]
        third_place_table.append({
            "Group": group_name,
            "Team": result["third"],
            **result["third_stats"]
        })

    third_df = pd.DataFrame(third_place_table)
    third_df = third_df.sort_values(by=["Points", "GD", "GF", "FairPlay"], ascending=False)

    if verbose:
        print("\nBEST THIRD PLACED TEAMS")
        print(third_df.head(8)[["Team", "Points", "GD", "GF", "FairPlay"]])

    best_third = third_df.head(8)
    best_third_dict = {}
    for _, row in best_third.iterrows():
        best_third_dict[row["Group"]] = row["Team"]

    qualified_teams = (
        list(group_winners.values()) +
        list(group_runners.values()) +
        best_third["Team"].tolist()
    )

    third_assignment = assign_third_place_teams(best_third_dict)

    round32 = []
    for g1, g2 in FIXED_RU_MATCHUPS:
        round32.append((group_runners[g1], group_runners[g2]))
    for gw, gr in FIXED_W_RU_MATCHUPS:
        round32.append((group_winners[gw], group_runners[gr]))
    for winner_group, third_team in third_assignment.items():
        round32.append((group_winners[winner_group], third_team))

    round16_teams = play_matchups(round32, match_history, "Round of 32")
    quarterfinals_teams = play_rounds(round16_teams, match_history, "Round of 16")
    semifinals_teams = play_rounds(quarterfinals_teams, match_history, "Quarterfinal")
    final_teams = play_rounds(semifinals_teams, match_history, "Semifinal")

    final_result = simulate.simulate(final_teams[0], final_teams[1], knockout=True)
    final_result["stage"] = "Final"
    final_result["match_id"] = len(match_history) + 1
    final_result["team1_code"] = TEAM_INFO[final_result["team1"]]["code"]
    final_result["team2_code"] = TEAM_INFO[final_result["team2"]]["code"]
    final_result["team1_logo"] = TEAM_INFO[final_result["team1"]]["logo"]
    final_result["team2_logo"] = TEAM_INFO[final_result["team2"]]["logo"]
    final_result["scoreline"] = (
        f"{final_result['team1']} "
        f"{final_result['goals1']}-{final_result['goals2']} "
        f"{final_result['team2']}"
    )
    match_history.append(final_result)

    champion = final_result["winner"]

    print(len(match_history))
    return {
        "champion": champion,
        "qualified_teams": qualified_teams,
        "round16": round16_teams,
        "quarterfinalists": quarterfinals_teams,
        "semifinalists": semifinals_teams,
        "finalists": final_teams,
        "match_history": match_history
    }


winner_count = {}
final_count = {}
semi_count = {}
quarter_count = {}
round16_count = {}

SIMULATIONS = 1000

tournament = simulate_world_cup(groups, verbose=True)

print("\nCHAMPION")
print(tournament["champion"])

print("\nTOTAL MATCHES")
print(len(tournament["match_history"]))

print("\nFIRST MATCH")
print(tournament["match_history"][0])

print("\nLAST MATCH")
print(tournament["match_history"][-1])