import logging
from random import randrange
from collections import namedtuple
from copy import deepcopy

from rules import take_round, player_has_models, player_model_count
from deployment import make_unit
from unit import Unit
from thoughts import thought_for_the_day
from stratgey import Strategy

def simulate_games(amount):
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
    avg_round, avg_winner = 0, 0
    player1_kia, player1_mia = 0, 0
    player2_kia, player2_mia = 0, 0
    for i in range(amount):
        round, winner, stats = simulate_game(players, deepcopy(units))
        avg_round += round
        avg_winner += winner
        player1_kia += stats[0]['KIA']
        player1_mia += stats[0]['MIA']
        player2_kia += stats[1]['KIA']
        player2_mia += stats[1]['MIA']
    print()
    print("Average rounds {}".format(avg_round / amount))
    print("{} win rate {}".format(players[1], avg_winner / amount))
    print("Average {}: KIA {}, MIA {}".format(players[0], player1_kia / amount, player1_mia / amount))
    print("Average {}: KIA {}, MIA {}".format(players[1], player2_kia / amount, player2_mia / amount))



def simulate_game(players, units):
    stats = (
        {'KIA': 0, 'MIA': 0, 'detailed': []},
        {'KIA': 0, 'MIA': 0, 'detailed': []},
    )
    won = False
    round = 1
    while not won:
        print("Round {}".format(round))
        won = take_round(players, units, stats)
        round += 1
    print()
    print("Finished in {} turns".format(round))
    if player_has_models(units, 0):
        print("{} Player Wins!, {} models left".format(players[0], player_model_count(units, 0)))
        winner = 0
    else:
        print("{} Player Wins!, {} models left".format(players[1], player_model_count(units, 1)))
        winner = 1
    for i, player in enumerate(players):
        print(player)
        print(stats[i])
    return round, winner, stats


simulate_games(10)
print(thought_for_the_day())
