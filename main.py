import logging
from random import randrange
from collections import namedtuple

SOURCE_URL = "https://raw.githubusercontent.com/BSData/wh40k/master/T\'au%20Empire.cat"

Model = namedtuple(
    'Model', [
        'name', 'movement', 'weapon_skill', 'ballistic_skill',
        'strength', 'toughness', 'wounds', 'attacks', 'leadership', 'armour'])

Weapon = namedtuple(
    'Weapon', ['name', 'range', 'type',
    'strength', 'armour_piercing', 'damage', 'abilities'])


def make_piece():
    return {
        'model': Model('guy', 6, 4, 4, 4, 4, 1, 1, 8, 5),
        'weapons': [
            Weapon('blaster', 36, 'assault 2', 5, 0, 1, None),
            Weapon('knife', 'melee', 'melee 1', 5, 0, 1, None)]
    }


def simulate_game():
    players = ['player 1', 'player 2']
    models = (
        {'pos': 0, 'unit': 5 * [make_piece()]},
        {'pos': 50, 'unit': 5 * [make_piece()]}
    )
    won = False
    round = 1
    while not won:
        print("Round {}".format(round))
        won = take_round(players, models)
        round += 1
    if len(models[0]['unit']) == 0:
        print("Player 2 Wins!")
    else:
        print("Player 1 Wins!")


def take_round(players, models):
    for i, p in enumerate(players):
        won = take_turn(i, p, models)
        if won:
            break
    return won


def take_turn(i, player, models):
    print("{}".format(player))
    print("====")
    print()
    move_phase(i, player, models)
    psychic_phase(i, player, models)
    shooting_phase(i, player, models)
    charge_phase(i, player, models)
    fight_phase(i, player, models)
    morale_phase(i, player, models)
    return len(models[0]['unit']) == 0 or len(models[1]['unit']) == 0


def roll_d6():
    return randrange(1, 6)


def get_seperation(models):
    return abs(models[1]['pos'] - models[0]['pos'])


def move_phase(i, player, models):
    seperation = get_seperation(models)
    movement = models[i]['unit'][0]['model'].movement
    range = models[i]['unit'][0]['weapons'][0].range
    direction = 1 if i == 0 else -1
    if seperation > movement + range:
        models[i]['pos'] += direction * (movement + roll_d6())
        logging.warning("Advance to {}".format(models[i]['pos']))
    elif seperation > range:
        models[i]['pos'] +=  direction * movement
        logging.warning("Move into range {}".format(models[i]['pos']))
    else:
        logging.warning("Hold position")


def psychic_phase(i, player, models):
    logging.warning("Does Nothing yet")


def wound_roll(strength, toughness):
    if strength > 2 * toughness:
        need = 2
    elif strength > toughness:
        need = 3
    elif strength == toughness:
        need = 4
    elif strength > toughness / 2:
        need = 5
    else:
        need = 6
    return roll_d6() >= need


def shooting_phase(i, player, models):
    opfor = 1 if i == 0 else 0
    for m in models[i]['unit']:
        for w in m['weapons']:
            if w.range != 'melee' and get_seperation(models) <= w.range:
                attacks = int(w.type.split(" ")[1])
                for a in range(attacks):
                    if len(models[opfor]['unit']):
                        if roll_d6() >= m['model'].ballistic_skill:
                            logging.warning("hits with {}!".format(w.name))
                            if wound_roll(w.strength, models[opfor]['unit'][0]['model'].toughness):
                                logging.warning("bam! wounds!")
                                if roll_d6() < models[opfor]['unit'][0]['model'].armour - w.armour_piercing:
                                    logging.warning("Armour fails!")
                                    if w.damage >= models[opfor]['unit'][0]['model'].wounds:
                                        om = models[opfor]['unit'].pop()
                                        logging.warning("{} is dead!".format(om['model'].name))

                                    else:
                                        # handle taking off wounds
                                        logging.warning("Injured but not dead!")
                                else:
                                    logging.warning("Armour saves!")
                            else:
                                logging.warning("Fails to wound")
                        else:
                            logging.warning("Miss!")


def charge_phase(i, player, models):
    logging.warning("Does Nothing yet")


def fight_phase(i, player, models):
    logging.warning("Does Nothing yet")


def morale_phase(i, player, models):
    logging.warning("Does Nothing yet")


simulate_game()
