import logging
from typing import Dict, Tuple, List, Any
from collections import defaultdict
from itertools import zip_longest
from copy import deepcopy

from rules import take_round, player_has_models, player_model_count
from deployment import make_unit, make_tank
from unit import Unit
from thoughts import thought_for_the_day
from stats import mean, get_stats

logging.basicConfig(level=logging.INFO)


def simulate_games(samples: int) -> Dict[str, Any]:
    """Runs a set of simulations to get some average stats"""
    player_names = ['Loyal', 'Traitor']
    units = (
        [
            make_unit("1st Sqd", 0, False),
            make_unit("2nd Sqd", 0, True),
            make_tank("Tank 1", 0, False)
        ],
        [
            make_unit("1st Sqd", 50, False),
            make_unit("2nd Sqd", 50, True),
            make_tank("Tank 1", 0, False)
        ],
    )
    options = {
        'reinforce_position_0': 0,
        'reinforce_position_1': 50
    }
    rounds, winner = [], []
    player1_kia, player1_mia = [], []
    player2_kia, player2_mia = [], []
    player1_killzone, player2_killzone = [], []
    player1_overkill: List[int] = []
    player2_overkill: List[int] = []
    player1_models, player2_models = [], []
    player1_units, player2_units = defaultdict(list), defaultdict(list)
    player1_weapons, player2_weapons = defaultdict(list), defaultdict(list)
    for i in range(samples):
        units_copy = [
            deepcopy(units[0]),
            deepcopy(units[1])
        ]
        round, win, stats = simulate_game(player_names, units_copy, options)
        rounds.append(float(round))
        winner.append(float(win))
        player1_kia.append(stats[0]['KIA'])
        player1_mia.append(stats[0]['MIA'])
        player2_kia.append(stats[1]['KIA'])
        player2_mia.append(stats[1]['MIA'])
        player1_killzone.extend(stats[0]['killzone'])
        player2_killzone.extend(stats[1]['killzone'])
        player1_overkill.extend(stats[0]['overkill'])
        player1_overkill.extend(stats[1]['overkill'])
        player1_models.append(stats[0]['models_per_turn'])
        player2_models.append(stats[1]['models_per_turn'])
        for k, v in stats[0]['damage_per_unit'].items():
            player1_units[k].append(v)
        for k, v in stats[0]['damage_per_weapon'].items():
            player1_weapons[k].append(v)
        for k, v in stats[1]['damage_per_unit'].items():
            player2_units[k].append(v)
        for k, v in stats[1]['damage_per_weapon'].items():
            player2_weapons[k].append(v)

    return {
        "round": get_stats(rounds),
        "player1_stats": {
            "name": player_names[0],
            "win_rate": 1 - mean(winner),
            "kia": get_stats(player1_kia),
            "mia": get_stats(player1_mia),
            "killzone": get_stats(player1_killzone),
            "overkill": get_stats(player1_overkill),
            "models_per_turn": [get_stats(units_in_nth_turn) for units_in_nth_turn in zip_longest(
                *player1_models)],
            "damage_per_unit": {k: get_stats(v) for k, v in player1_units.items()},
            "damage_per_weapon": {k: get_stats(v) for k, v in player1_weapons.items()}
        },
        "player2_stats": {
            "name": player_names[1],
            "win_rate": mean(winner),
            "kia": get_stats(player2_kia),
            "mia": get_stats(player2_mia),
            "killzone": get_stats(player2_killzone),
            "overkill": get_stats(player2_overkill),
            "models_per_turn": [get_stats(units_in_nth_turn) for units_in_nth_turn in zip_longest(
                *player2_models)],
            "damage_per_unit": {k: get_stats(v) for k, v in player2_units.items()},
            "damage_per_weapon": {k: get_stats(v) for k, v in player2_weapons.items()}
        }
    }


def simulate_game(player_names: List[str], units: List[List[Unit]], options)\
        -> Tuple[int, int, Any]:
    """Runs one game"""
    stats: List[Dict[str, Any]] = [
        {'KIA': 0, 'MIA': 0, 'troops_per_turn': [], 'killzone': [], 'overkill': [],
         'models_per_turn': [],
         'damage_per_unit': defaultdict(lambda: 0), 'damage_per_weapon': defaultdict(lambda: 0)},
        {'KIA': 0, 'MIA': 0, 'troops_per_turn': [], 'killzone': [], 'overkill': [],
         'models_per_turn': [],
         'damage_per_unit': defaultdict(lambda: 0), 'damage_per_weapon': defaultdict(lambda: 0)},
    ]
    won = False
    round = 1
    while not won:
        logging.info("Round {}".format(round))
        for i in range(0, 2):
            stats[i]['models_per_turn'].append(player_model_count(units, i))
        won = take_round(player_names, units, stats, options)
        round += 1
    for i in range(0, 2):
        stats[i]['models_per_turn'].append(player_model_count(units, i))
    logging.info("")
    logging.info("Finished in {} turns".format(round))
    winner = 0 if player_has_models(units, 0) else 1
    logging.info("{} Player Wins!, {} models left".format(
        player_names[winner], player_model_count(units, winner)))
    return round, winner, stats


if __name__ == "__main__":
    print(simulate_games(10))
    print(thought_for_the_day())
