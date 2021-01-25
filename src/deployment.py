from typing import Dict
from copy import deepcopy
from itertools import chain

from unit import Unit, Model, ModelStats, Weapon, DamageTable
from stratgey import Strategy
from names import generate_name


def make_unit_from_bs(
        name: str, id: str, selector: Dict, cat: Dict, position: int, strategy: Strategy, off_board: bool):
    """This converst a bs json into a unit for simulation"""
    assert cat[id]['target_type'] == 'selectionEntry'
    unit = resolve_links(cat[id]['link_target'])
    assert unit['type'] == 'unit'

    models = []
    for s, sub_selections in selector.items():
        for i in range(sub_selections[0]):
            models.append(make_model_from_bs(i, s, sub_selections, unit))

    return Unit(
        name,
        cat[id]['name'] or unit['name'],
        position,
        strategy,
        models,
        set(unit['category_links']),
        off_board
    )


def make_model_from_bs(i: int, s: str, sub_selections, unit: Dict):
    """This converts a bs json into a model for simulation"""
    selection = unit['selection_entries'][s]
    model = [p for p in selection['profiles'] if p['profile_type'] == 'Unit']
    assert len(model) == 1
    name = selection['name'] or model[0]['name']
    # if 'Heavy Weapon' in name:
    #     import pdb
    #     pdb.set_trace()
    weapons = resolve_weapons(selection, sub_selections)
    return Model(
        ModelStats(
            "{} {}".format(name, i),
            int(model[0]['M'].replace('"', '')),
            int(model[0]['WS'].replace('+', '')),
            int(model[0]['BS'].replace('+', '')),
            int(model[0]['S']),
            int(model[0]['T']),
            int(model[0]['W']),
            int(model[0]['A']),
            int(model[0]['Ld']),
            int(model[0]['Save'].replace('+', ''))
        ),
        [],
        [],
        [],  # not sure how this is gonna look like callbacks?
        weapons
    )


def resolve_weapons(selection: Dict, sub_selections):
    """Converts the dictionary into a list of weapons"""
    weapons = []
    # import pdb
    # pdb.set_trace()
    for s in selection['selection_entries'].values():
        weapons.extend(resolve_weapons(s, sub_selections))
    for s in selection['selection_entry_groups'].values():
        weapons.extend(resolve_weapons(s, sub_selections))
    for p in  selection['profiles']:
        if p['profile_type'] == 'Weapon' and selection['id'] in sub_selections[1]:
            name = selection['name'] or p['name']
            weapons.append(
                Weapon(name, p['Range'].replace('"', ''), p['Type'],
                p['S'], p['AP'], p['D'], p['Abilities'])
            )
    return weapons


labels = {
    "selectionEntry": "selection_entries",
    "profile": "profiles",
    "selectionEntryGroup": "selection_entry_groups",
}


def remove_empty_links(selection_entry: Dict):
    """Make life easier debugging removes empty items"""
    selection = deepcopy(selection_entry)
    if type(selection) == dict:
        for k, v in selection.items():
            if type(v) in (dict, list):
                selection[k] = remove_empty_links(v)
    elif type(selection) == list:
        for i, v in enumerate(selection):
            if type(v) in (dict, list):
                selection[i] = remove_empty_links(v)
    keys_to_remove = []
    if type(selection) == dict:
        for k, v in selection.items():
            if v in ([], {}):
                keys_to_remove.append(k)
        for k in keys_to_remove:
            del selection[k]
    elif type(selection) == list:
        for i, v in enumerate(selection):
            if v in ([], {}):
                selection.pop(i)
    return selection


def resolve_links(selection_entry: Dict):
    """Turns links into regular values"""
    selection = deepcopy(selection_entry)
    for section in ('entry_links', 'info_links'):
        if selection.get(section):
            for k, v in selection[section].items():
                assert k not in selection_entry['selection_entries'].keys(), "key {} already in {}".format(k, v["target_type"])
                if v["target_type"] == 'selectionEntry':
                    selection[labels[v["target_type"]]][k] = v['link_target']
                elif v["target_type"] == 'profile':
                    selection[labels[v["target_type"]]].append(v['link_target'])
                elif v["target_type"] == 'selectionEntryGroup':  # TODO change groups to dicts in XSLT
                    selection[labels[v["target_type"]]][k] = v['link_target']
            selection[section] = {}
    # resolve all the selections inside this
    for k, v in selection['selection_entries'].items():
        selection['selection_entries'][k] = resolve_links(v)
    if selection.get('selection_entry_groups'):
        for k, v in selection['selection_entry_groups'].items():
            selection['selection_entry_groups'][k] = resolve_links(v)
    return selection


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
