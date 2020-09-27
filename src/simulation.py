import logging
from typing import Dict, Tuple, List, Any
from random import randrange
from collections import namedtuple, defaultdict
from copy import deepcopy
import logging

from rules import take_round, player_has_models, player_model_count
from deployment import make_unit
from unit import Unit
from thoughts import thought_for_the_day
from stratgey import Strategy
from stats import mean, get_stats


def simulate_games(amount: int) -> Dict[str, Any]:
    players = ['Loyal', 'Traitor']
    units = (
        [
            make_unit("1st Sqd", 0),
            make_unit("2nd Sqd", 0)
        ],
        [
            make_unit("1st Sqd", 50),
            make_unit("2nd Sqd", 50)
        ],
    )
    rounds, winner = [], []
    player1_kia, player1_mia = [], []
    player2_kia, player2_mia = [], []
    player1_units, player2_units = defaultdict(list), defaultdict(list)
    player1_weapons, player2_weapons = defaultdict(list), defaultdict(list)
    for i in range(amount):
        round, win, stats = simulate_game(players, deepcopy(units))
        rounds.append(round)
        winner.append(win)
        player1_kia.append(stats[0]['KIA'])
        player1_mia.append(stats[0]['MIA'])
        player2_kia.append(stats[1]['KIA'])
        player2_mia.append(stats[1]['MIA'])
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
            "name": players[0],
            "win_rate": 1 - mean(winner),
            "kia": get_stats(player1_kia),
            "mia": get_stats(player1_mia),
            "damage_per_unit": {k: get_stats(v) for k, v in player1_units.items()},
            "damage_per_weapon": {k: get_stats(v) for k, v in player1_weapons.items()}
        },
        "player2_stats": {
            "name": players[1],
            "win_rate": mean(winner),
            "kia": get_stats(player2_kia),
            "mia": get_stats(player2_mia),
            "damage_per_unit": {k: get_stats(v) for k, v in player2_units.items()},
            "damage_per_weapon": {k: get_stats(v) for k, v in player2_weapons.items()}
        }
    }


def simulate_game(players: List[str], units: List[List[Unit]]) -> Tuple[int, int, Dict[str, Any]]:
    stats = (
        {'KIA': 0, 'MIA': 0, 'troops_per_turn': [], 'killzone': [],
        'damage_per_unit': defaultdict(lambda : 0), 'damage_per_weapon': defaultdict(lambda : 0)},
        {'KIA': 0, 'MIA': 0, 'troops_per_turn': [], 'killzone': [],
        'damage_per_unit': defaultdict(lambda : 0), 'damage_per_weapon': defaultdict(lambda : 0)},
    )
    won = False
    round = 1
    while not won:
        logging.info("Round {}".format(round))
        won = take_round(players, units, stats)
        round += 1
    logging.info("")
    logging.info("Finished in {} turns".format(round))
    if player_has_models(units, 0):
        logging.info("{} Player Wins!, {} models left".format(players[0], player_model_count(units, 0)))
        winner = 0
    else:
        logging.info("{} Player Wins!, {} models left".format(players[1], player_model_count(units, 1)))
        winner = 1
    return round, winner, stats


if __name__ == "__main__":
    print(simulate_games(10))
    print(thought_for_the_day())
