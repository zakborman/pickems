import random

# Function to simulate a match between two teams
def simulate_match(team1, team2):
    rating1 = team1[1]
    rating2 = team2[1]
    prob_team1_wins = rating1 / (rating1 + rating2)
    return random.random() < prob_team1_wins

# Function to pair teams in the first round using the alternative method
def pair_first_round_alternative(teams):
    pairs = []
    for i in range(8):
        pairs.append((teams[i], teams[i + 8]))
    return pairs

# Function to pair teams in each round
def pair_teams(records, teams, qualified, eliminated):
    # Group teams by their current win-loss records
    current_round_teams = [team for team in teams if team[0] not in qualified and team[0] not in eliminated]
    
    # Create a dictionary to hold teams grouped by their records
    record_groups = {}
    for team in current_round_teams:
        record = records[team[0]]
        if record not in record_groups:
            record_groups[record] = []
        record_groups[record].append(team)
    
    # Sort teams within each record group by their initial seed (original order)
    for record in record_groups:
        record_groups[record].sort(key=lambda team: teams.index(team))
    
    pairs = []
    # Pair the teams within each record group
    for record in sorted(record_groups.keys(), reverse=True):
        group = record_groups[record]
        while len(group) >= 2:
            team1 = group.pop(0)
            team2 = group.pop(-1)
            pairs.append((team1, team2))
    
    return pairs

# Function to run a single simulation of the Swiss system tournament
def run_tournament(teams, stats, alternative_first_round=False):
    # Initialize the win/loss records
    records = {team[0]: 0 for team in teams}
    losses = {team[0]: 0 for team in teams}
    qualified = set()
    eliminated = set()
    
    # Pair teams for the first round
    if alternative_first_round:
        pairs = pair_first_round_alternative(teams)
    else:
        pairs = [(teams[i], teams[15 - i]) for i in range(8)]
    
    # Simulate the first round
    for team1, team2 in pairs:
        if simulate_match(team1, team2):
            records[team1[0]] += 1
            losses[team2[0]] += 1
        else:
            records[team2[0]] += 1
            losses[team1[0]] += 1
    
    # Continue with the remaining rounds
    while len(qualified) + len(eliminated) < 16:
        pairs = pair_teams(records, teams, qualified, eliminated)
        
        for team1, team2 in pairs:
            if simulate_match(team1, team2):
                records[team1[0]] += 1
                losses[team2[0]] += 1
                if records[team1[0]] == 3:
                    qualified.add(team1[0])
                    stats[team1[0]]["qualify"] += 1
                    if records[team1[0]] == 3 and losses[team1[0]] == 0:
                        stats[team1[0]]["3-0"] += 1
                if losses[team2[0]] == 3:
                    eliminated.add(team2[0])
                    if losses[team2[0]] == 3 and records[team2[0]] == 0:
                        stats[team2[0]]["0-3"] += 1
            else:
                records[team2[0]] += 1
                losses[team1[0]] += 1
                if records[team2[0]] == 3:
                    qualified.add(team2[0])
                    stats[team2[0]]["qualify"] += 1
                    if records[team2[0]] == 3 and losses[team2[0]] == 0:
                        stats[team2[0]]["3-0"] += 1
                if losses[team1[0]] == 3:
                    eliminated.add(team1[0])
                    if losses[team1[0]] == 3 and records[team1[0]] == 0:
                        stats[team1[0]]["0-3"] += 1

# Function to simulate the tournament and calculate probabilities
def simulate_tournament(teams, alternative_first_round=False, num_simulations=100000):
    # Initialize statistics
    stats = {team[0]: {"3-0": 0, "0-3": 0, "qualify": 0} for team in teams}

    # Run multiple simulations to estimate probabilities
    for _ in range(num_simulations):
        run_tournament(teams, stats, alternative_first_round)

    # Calculate probabilities and convert to percentages
    for team in teams:
        team_name = team[0]
        stats[team_name]["3-0"] = (stats[team_name]["3-0"] / num_simulations) * 100
        stats[team_name]["0-3"] = (stats[team_name]["0-3"] / num_simulations) * 100
        stats[team_name]["qualify"] = (stats[team_name]["qualify"] / num_simulations) * 100

    # Output results in descending order of qualification probability
    sorted_teams = sorted(stats.items(), key=lambda x: x[1]["qualify"], reverse=True)
    print(f"{'Team':<20}{'Qualify (%)':>15}{'3-0 (%)':>15}{'0-3 (%)':>15}")
    for team, data in sorted_teams:
        print(f"{team:<20}{data['qualify']:>15.2f}{data['3-0']:>15.2f}{data['0-3']:>15.2f}")

# Define the teams and their ratings
katowice2019_challengers = [
    ("Fnatic", 237),
    ("NRG", 265),
    ("Cloud9", 208),
    ("Ninjas in Pyjamas", 163),
    ("ENCE", 182),
    ("Team Vitality", 162),
    ("G2 Esports", 109),
    ("AVANGAR", 114),
    ("Renegades", 166),
    ("Vega Squadron", 37),
    ("TYLOO", 27),
    ("Team Spirit", 115),
    ("FURIA", 80),
    ("Grayhound", 82),
    ("Winstrike", 74),
    ("ViCi", 62)
]
katowice2019_legends = [
    ("Astralis", 933),
    ("Team Liquid", 572),
    ("Natus Vincere", 412),
    ("MIBR", 230),
    ("FaZe Clan", 306),
    ("NRG", 332),
    ("BIG", 180),
    ("ENCE", 250),
    ("Renegades", 257),
    ("Team Vitality", 223),
    ("Ninjas in Pyjamas", 283),
    ("HellRaisers", 105),
    ("Cloud9", 262),
    ("G2 Esports", 166),
    ("AVANGAR", 167),
    ("compLexity", 52)
]



berlin2019_challengers = [
    ("Team Vitality", 490),
    ("NRG Esports", 279),
    ("North", 139),
    ("G2 Esports", 226),
    ("FURIA Esports", 221),
    ("mousesports", 203),
    ("AVANGAR", 41),
    ("CR4ZY", 87),
    ("Grayhound Gaming", 53),
    ("Complexity Gaming", 42),
    ("forZe", 61),
    ("HellRaisers", 30),
    ("TYLOO", 35),
    ("INTZ", 34),
    ("DreamEaters", 31),
    ("Syman Gaming", 25)
]
berlin2019_legends = [
    ("Astralis", 361),
    ("Team Liquid", 1000),
    ("ENCE", 328),
    ("Natus Vincere", 272),
    ("FaZe Clan", 263),
    ("Team Vitality", 472),
    ("MIBR", 136),
    ("Renegades", 78),
    ("NRG Esports", 294),
    ("Ninjas in Pyjamas", 147),
    ("North", 169),
    ("mousesports", 231),
    ("G2 Esports", 245),
    ("AVANGAR", 67),
    ("CR4ZY", 118),
    ("DreamEaters", 70)
]



paris2023_legends = [
    ("Natus Vincere", 806),
    ("9INE", 189),
    ("FURIA Esports", 369),
    ("Fnatic", 215),
    ("Heroic", 926),
    ("Into the Breach", 92),
    ("Team Vitality", 893),
    ("Bad News Eagles", 157),
    ("ENCE", 318),
    ("G2 Esports", 725),
    ("Apeks", 120),
    ("FaZe Clan", 700),
    ("Ninjas in Pyjamas", 221),
    ("Monte", 144),
    ("Team Liquid", 421),
    ("GamerLegion", 76)
]



copenhagen2024_opening = [
    ("Cloud9", 298),
    ("Eternal Fire", 229),
    ("ENCE", 305),
    ("Apeks", 218),
    ("Heroic", 226),
    ("GamerLegion", 200),
    ("SAW", 134),
    ("FURIA", 184),
    ("ECSTATIC", 65),
    ("The MongolZ", 83),
    ("Imperial", 62),
    ("paiN", 45),
    ("Lynn Vision", 39),
    ("AMKAL", 75),
    ("KOI", 74),
    ("Legacy", 55)
]
copenhagen2024_elimination = [
    ("FaZe Clan", 926),
    ("Team Spirit", 747),
    ("Vitality", 709),
    ("MOUZ", 565),
    ("Complexity", 226),
    ("Virtus.pro", 367),
    ("Natus Vincere", 433),
    ("G2 Esports", 471),
    ("Heroic", 252),
    ("Cloud9", 301),
    ("Eternal Fire", 222),
    ("ECSTATIC", 71),
    ("paiN Gaming", 60),
    ("Imperial Esports", 75),
    ("The MongolZ", 95),
    ("FURIA", 182)
]



# austin2025_stage1 = [
#     ("COL", 98),
#     ("HEROIC", 117),
#     ("B8", 48),
#     ("BetBoom", 28),
#     ("TYLOO", 36),
#     ("LVG", 30),
#     ("Wildcard", 46),
#     ("FLY", 49),
#     ("OG", 21),
#     ("CW", 23),
#     ("Imperial", 22),
#     ("Nemiga", 18),
#     ("NRG", 26),
#     ("Legacy", 29),
#     ("MZP", 13),
#     ("Fluxo", 18)
# ]
# austin2025_stage2 = [
#     ("Falcons", 496),
#     ("FaZe", 177),
#     ("3DMAX", 118),
#     ("VP", 129),
#     ("paiN", 56),
#     ("FURIA", 115),
#     ("MIBR", 96),
#     ("M80", 35),
#     ("B8", 48),
#     ("HEROIC", 117),
#     ("BetBoom", 28),
#     ("OG", 21),
#     ("Nemiga", 18),
#     ("LVG", 30),
#     ("Legacy", 29),
#     ("TYLOO", 36)
# ]
# austin2025_stage3 = [
#     ("Vitality", 1000),
#     ("MOUZ", 571),
#     ("Spirit", 540),
#     ("G2", 251),
#     ("MongolZ", 387),
#     ("Aurora", 370),
#     ("NAVI", 294),
#     ("Liquid", 172),
#     ("Legacy", 60),
#     ("VP", 134),
#     ("paiN", 59),
#     ("3DMAX", 115),
#     ("FURIA", 125),
#     ("FaZe", 167),
#     ("Nemiga", 42),
#     ("LVG", 53)
# ]



austin2025_stage1 = [
    ("COL", 1433),
    ("HEROIC", 1552),
    ("B8", 1275),
    ("BetBoom", 1102),
    ("TYLOO", 1358),
    ("LVG", 1212),
    ("Wildcard", 1037),
    ("FLY", 1213),
    ("OG", 1097),
    ("CW", 1087),
    ("Imperial", 1074),
    ("Nemiga", 1045),
    ("NRG", 1121),
    ("Legacy", 1035),
    ("MZP", 959),
    ("Fluxo", 999)
]
austin2025_stage2 = [
    ("Falcons", 1890),
    ("FaZe", 1608),
    ("3DMAX", 1582),
    ("VP", 1449),
    ("paiN", 1223),
    ("FURIA", 1455),
    ("MIBR", 1357),
    ("M80", 1026),
    ("B8", 1368),
    ("HEROIC", 1651),
    ("BetBoom", 1188),
    ("OG", 1201),
    ("Nemiga", 1145),
    ("LVG", 1274),
    ("Legacy", 1112),
    ("TYLOO", 1396)
]
austin2025_stage3 = [
    ("Vitality", 2118),
    ("MOUZ", 1911),
    ("Spirit", 1899),
    ("G2", 1641),
    ("MongolZ", 1800),
    ("Aurora", 1764),
    ("NAVI", 1626),
    ("Liquid", 1532),
    ("Legacy", 1245),
    ("VP", 1522),
    ("paiN", 1341),
    ("3DMAX", 1608),
    ("FURIA", 1519),
    ("FaZe", 1613),
    ("Nemiga", 1243),
    ("LVG", 1387)
]

simulate_tournament(austin2025_stage3, True)
