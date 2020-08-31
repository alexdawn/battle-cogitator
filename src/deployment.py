from unit import Unit, Model, Weapon
from stratgey import Strategy
from names import generate_name


def make_unit(name, pos):
    return Unit(name, 'troopers', pos, Strategy.CHARGE, [
        make_piece("Sergent {}".format(generate_name()), 1, 0),
        make_piece("Gunner {}".format(generate_name()), 0, 1)] + [
        make_piece("Guardsman {}".format(generate_name()), 0, 0) for i in range(8)])


def make_piece(name, leader, heavy):
    leadership = 8
    if leader:
        leadership += 1
        weapons = [
            Weapon('laspistol', 18, 'pistol 1', 4, 0, 1, None),
            Weapon('grenade', 8, 'grenade D3', 8, -1, 1, None),
            Weapon('chainsword', 'melee', 'melee 2', 5, -1, 1, None)
        ]
    elif heavy:
        weapons = [
            Weapon('rocket', 36, 'heavy 1', 8, -2, 1, None),
            Weapon('grenade', 8, 'grenade D3', 8, -1, 1, None),
            Weapon('knife', 'melee', 'melee 1', 4, 0, 1, None)
        ]
    else:
        weapons = [
            Weapon('lasgun', 36, 'assault 2', 5, 0, 1, None),
            Weapon('grenade', 8, 'grenade D3', 8, -1, 1, None),
            Weapon('knife', 'melee', 'melee 1', 4, 0, 1, None)
        ]  # change to user strength, attacks]
    return {
        'model': Model(name, 6, 4, 4, 4, 4, 1, 1, leadership, 5),
        'powers': [],
        'abilities': [],  # not sure how this is gonna look like callbacks?
        'weapons': weapons
    }
