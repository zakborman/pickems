def win_prob(team1_points, team2_points):
    return team1_points / (team1_points + team2_points)

def simulate(teams, matchups):
    results = []

    for team1, team2 in matchups:
        team1_points = teams[team1]
        team2_points = teams[team2]

        prob_team1_wins = win_prob(team1_points, team2_points)
        prob_team2_wins = win_prob(team2_points, team1_points)

        results.append((team1, prob_team1_wins))
        results.append((team2, prob_team2_wins))

    # Sort results by probability in descending order
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)

    # Print results
    for team, prob in sorted_results:
        print(f"{team}: {prob:.2f}")

# Teams and matchups as provided
teams_legends_rio2022 = {
    "FaZe": 819,
    "Vitality": 756,
    "Liquid": 741,
    "Natus Vincere": 660,
    "Cloud9": 595,
    "Heroic": 476,
    "Outsiders": 431,
    "MOUZ": 403,
    "FURIA": 381,
    "Ninjas in Pyjamas": 336,
    "ENCE": 322,
    "Spirit": 322,
    "BIG": 204,
    "Fnatic": 156,
    "Bad News Eagles": 122,
    "Sprout": 92
}
matchups_legends_rio2022 = [
    ("Liquid", "MOUZ"),
    ("Spirit", "Bad News Eagles"),
    ("FaZe", "Cloud9"),
    ("Sprout", "BIG"),
    ("Natus Vincere", "Vitality"),
    ("Heroic", "Outsiders"),
    ("ENCE", "FURIA"),
    ("Ninjas in Pyjamas", "Fnatic")
]

teams_legends_paris2023 = {
    "Heroic": 926,
    "Vitality": 893,
    "Liquid": 421,
    "Monte": 144,
    "GamerLegion": 76,
    "Apeks": 120,
    "Into the Breach": 92,
    "FaZe Clan": 700,
    "Natus Vincere": 806,
    "Fnatic": 215,
    "Ninjas in Pyjamas": 221,
    "ENCE": 318,
    "Bad News Eagles": 157,
    "G2 Esports": 725,
    "9INE": 189,
    "FURIA": 369
}
matchups_legends_paris2023 = [
    ("Natus Vincere", "GamerLegion"),
    ("9INE", "Liquid"),
    ("FURIA", "Monte"),
    ("Fnatic", "Ninjas in Pyjamas"),
    ("Heroic", "FaZe Clan"),
    ("Into the Breach", "Apeks"),
    ("Vitality", "G2 Esports"),
    ("Bad News Eagles", "ENCE")
]

simulate(teams_legends_paris2023, matchups_legends_paris2023)