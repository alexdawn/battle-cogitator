from unit import Unit, Model, ModelStats, Weapon, DamageTable
from stratgey import Strategy
from names import generate_name


def make_unit(name: str, pos: int, off_board: bool) -> Unit:
    """Template function to construct a unit"""
    return Unit(name, 'troopers', pos, Strategy.CHARGE, [
        make_piece("Sergent {}".format(generate_name()), True, False),
        make_piece("Gunner {}".format(generate_name()), False, True)] + [
        make_piece("Guardsman {}".format(generate_name()), False, False) for i in range(8)],
        {'infantry'}, off_board)


def make_tank(name: str, pos: int, off_board: bool) -> Unit:
    """Example tank to check heavy guns, blast and damage tables"""
    return Unit(name, 'Tank', pos, Strategy.HOLD, [
        Model(
            ModelStats("Tank", 12, "-", 3, 8, 8, 10, "-", 10, 3),
            [
                DamageTable(6, 10, {"ballistic_skill": 3, "movement": 12}),
                DamageTable(3, 5, {"ballistic_skill": 4, "movement": 8}),
                DamageTable(0, 2, {"ballistic_skill": 5, "movement": 6})
            ], [], [], [
                Weapon('Main Cannon', 72, 'heavy 1', 8, 0, 'D6', 'blast'),
                Weapon('Lascannon', 48, 'heavy 2', 8, -2, 'D3', None),
                Weapon('Heavy Bolter', 23, 'heavy 3', 7, 0, '1', None),
            ]
        )
    ], {'vehicle'}, False)


def make_piece(name: str, leader: bool, heavy: bool) -> Model:
    """Template function to create a model piece"""
    leadership = 8
    if leader:
        leadership += 1
        weapons = [
            Weapon('laspistol', 18, 'pistol 1', 4, 0, '1', None),
            Weapon('grenade', 8, 'grenade 6', 8, -1, '1', 'blast'),
            Weapon('chainsword', 'melee', 'melee 2', 5, -1, '1', None)
        ]
    elif heavy:
        weapons = [
            Weapon('rocket', 36, 'heavy 1', 8, -2, '1', None),
            Weapon('grenade', 8, 'grenade D6', 8, -1, '1', 'blast'),
            Weapon('knife', 'melee', 'melee 1', 4, 0, '1', None)
        ]
    else:
        weapons = [
            Weapon('lasgun', 36, 'assault 2', 5, 0, '1', None),
            Weapon('grenade', 8, 'grenade D6', 8, -1, '1', 'blast'),
            Weapon('knife', 'melee', 'melee 1', 4, 0, '1', None)
        ]  # change to user strength, attacks]
    return Model(
        ModelStats(name, 6, 4, 4, 4, 4, 1, 1, leadership, 5),
        [],
        [],
        [],  # not sure how this is gonna look like callbacks?
        weapons
    )
