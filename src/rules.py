from random import randrange
from typing import Tuple, List
from itertools import zip_longest

from unit import Unit
from stratgey import Strategy, get_strategy_function


def take_round(players: Tuple[str], units: Tuple[List[Unit]], stats) -> bool:
    """Play a round for each player"""
    for i, p in enumerate(players):
        for x, y in enumerate(players):
            for unit in units[x]:  # reset states
                unit.reset()
        won = take_turn(i, p, units, stats)
        if won:
            break
    return won


def player_model_count(units: Tuple[List[Unit]], i: int) -> int:
    """Get count of models player has"""
    return sum(len(u.models) for u in units[i])


def player_has_models(units: Tuple[List[Unit]], i: int) -> bool:
    """Does player have any models left?"""
    return player_model_count(units, i) > 0


def take_turn(i: int, player: str, units: Tuple[List[Unit]], stats) -> bool:
    """Run through each phase"""
    print("{}".format(player))
    print("====")
    move_phase(i, units)
    psychic_phase(i, units, stats)
    shooting_phase(i, units, stats)
    charge_phase(i, units, stats)
    fight_phase(i, units, stats)
    morale_phase(i, units, stats)
    return not player_has_models(units, 0) or not player_has_models(units, 1)


def roll_d(x) -> int:
    """Roll a DX"""
    return randrange(1, x)


def get_seperation(unit1: Unit, unit2: Unit) -> float:
    """Get Distance between two units"""
    return unit2.pos - unit1.pos


def get_nearest_opposing_unit(unit: Unit, opfor: int, units: Tuple[List[Unit]]) -> Unit:
    """Find the nearest opposing unit"""
    opossed = sorted(units[opfor], key=lambda ou: get_seperation(unit, ou))
    if opossed:
        return opossed[0]


def get_opfor(i: int) -> int:
    """Get the player index for the opposition player"""
    return 1 if i == 0 else 0


def move_phase(i: int, units: Tuple[List[Unit]]):
    """Move a players models"""
    for unit in units[i]:
        if unit.models:
            opossing_unit = get_nearest_opposing_unit(unit,  get_opfor(i), units)
            seperation = get_seperation(unit, opossing_unit)
            direction = 1 if seperation > 0 else -1
            movement = unit.unit_movement()
            strat = get_strategy_function(unit.strategy)
            strat(unit, abs(seperation), direction)


def psychic_phase(i: int, units: Tuple[List[Unit]], stats) -> None:
    """Cast psychic powers"""
    for unit in units[i]:
        for u, m in enumerate(unit.models):
            for w in m['powers']:
                logging.warning("No psykers yet")


def wound_roll(strength: int, toughness: int) -> bool:
    """Use the wound chart, then do a wound roll"""
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
    return roll_d(6) >= need


def pick_target():
    # pick nearest enemy not in combat
    pass


def choose_weapon(unit, seperation, weapons):
    # choose non-pistol if option, model with weakest wepaon the grenade
    if abs(seperation) <= 1:
        return [w for w in weapons if "pistol" in w.type]
    if not unit.has_used_grenade:
        return [w for w in weapons if "grenade" in w.type]
    else:
        return [w for w in weapons if "pistol" not in w.type and "grenade" not in w.type]


def resolve_attacks():
    pass


def can_attack(unit: Unit, seperation: float, weapon_type: str):
    """Check movement to see if weapon type can attack"""
    if unit.moved == 'advanced' and weapon_type == 'assault':
        return True
    elif unit.moved != 'advanced' and seperation > 1:
        return True
    elif unit.moved != 'advanced' and weapon_type == 'pistol':
        return True
    else:
        return False


def aim_penalty(unit: Unit, weapon_type: str):
    """Check movement to see if there are aim penalties"""
    if unit.moved == 'advanced' and weapon_type == 'assault':
        return -1
    elif unit.moved != 'moved' and weapon_type == 'heavy':
        return -1
    else:
        return 0


def resolve_die_notation(text: str) -> int:
    """Resolve variable attacks notation"""
    if 'D' in text:
        if 'D3':
            return roll_d(3)
        elif 'D6':
            return roll_d(6)
        else:
            raise RuntimeError("Unknown format")
    else:
        return int(text)


def flavour_text(weapon_type):
    texts = {
        'rapid_fire': 'double taps with a',
        'assault': 'sprays with a',
        'heavy': 'blasts with a',
        'grenade': 'lobs a',
        'pistol': 'draws and fires a',
    }
    return texts[weapon_type]


def shoot_with_unit(i, units, unit, stats, is_overwatch=False, charging_unit=None):
    """Do shots with a unit"""
    # handle grenade or other weapons
    # handle rapid fire
    opfor = get_opfor(i)
    if len(units[opfor]):
        opossing_unit = charging_unit if is_overwatch else get_nearest_opposing_unit(unit, opfor, units)
        sep = get_seperation(unit, opossing_unit)
        for u, m in enumerate(unit.models):
            for w in choose_weapon(unit, sep, m['weapons']):
                weapon_type, attack_notation = w.type.split(" ")
                attacks = resolve_die_notation(attack_notation)
                if weapon_type == 'rapid_fire' and abs(sep) <= w.range / 2:
                    print("Rapid fire weapon is at close range, twice the attacks")
                    attacks *= 2
                if (w.range != 'melee'
                    and (weapon_type != 'grenade' or not unit.has_used_grenade)
                    and can_attack(unit, abs(sep), weapon_type)
                    and abs(sep) <= w.range):
                    if weapon_type == 'grenade':
                        unit.has_used_grenade = True
                    for a in range(int(attacks)):
                        if len(opossing_unit.models):
                            opossing_unit = get_nearest_opposing_unit(unit, opfor, units)
                            sep = get_seperation(unit, opossing_unit)
                            message = []
                            message.append("{} {} {}".format(m['model'].name, flavour_text(weapon_type), w.name))
                            hit_value = m['model'].ballistic_skill + aim_penalty(unit, weapon_type)
                            if roll_d(6) >= (6 if is_overwatch else hit_value):
                                message.append("Hits!")
                                if wound_roll(w.strength, opossing_unit.unit_toughness()):  # this errored
                                    message.append("Wounds!")
                                    if roll_d(6) < opossing_unit.models[0]['model'].armour - w.armour_piercing:
                                        message.append("Armour fails!")
                                        if opossing_unit.take_damage(w.damage, message):
                                            stats[opfor]['KIA'] += 1
                                        if len(opossing_unit.models) == 0:
                                            message.append("\nUnit wiped out!")
                                            units[opfor].remove(opossing_unit)
                                    else:
                                        message.append("Armour saves!")
                                else:
                                    message.append("Fails to wound")
                            else:
                                message.append("Miss!")
                            print(" ".join(message))


def shooting_phase(i, units, stats):
    for unit in units[i]:
        shoot_with_unit(i, units, unit, stats)


def charge_phase(i, units, stats):
    """Do charge phase"""
    opfor = get_opfor(i)
    direction = 1 if i == 0 else -1
    for unit in units[i]:
        if unit.models and unit.strategy in (Strategy.CHARGE, Strategy.HCHARGE):
            opossing_unit = get_nearest_opposing_unit(unit,  get_opfor(i), units)
            if opossing_unit:
                seperation = abs(get_seperation(unit, opossing_unit))
                if units[i] and seperation <= 12 and seperation > 1:
                    print("Defender fires in overwatch...")
                    shoot_with_unit(opfor, units, opossing_unit, stats, is_overwatch=True, charging_unit=unit)
                    charge = roll_d(6) + roll_d(6)
                    if charge >= seperation:
                        print("Charge success {}".format(charge))
                        unit.pos += direction * min(charge, seperation)
                    else:
                        print("Charge failed rolled {}, but needed {}".format(charge, seperation))


def combat(i: int, units, unit, stats):
    """Enact the combat for one unit"""
    opfor = get_opfor(i)
    if len(units[opfor]):
        opossing_unit = get_nearest_opposing_unit(unit, opfor, units)
        sep = get_seperation(unit, opossing_unit)
        if abs(sep) <= 1:
            for u, m in enumerate(unit.models):
                for w in m['weapons']:
                    weapon_type, attacks = w.type.split(" ")
                    if w.range == 'melee':
                        for a in range(int(attacks)):
                            if len(opossing_unit.models):
                                message = []
                                if roll_d(6) >= m['model'].weapon_skill:
                                    message.append("hits with {}!".format(w.name))
                                    if wound_roll(w.strength, opossing_unit.models[0]['model'].toughness):
                                        message.append("Wounds!")
                                        if roll_d(6) < opossing_unit.models[0]['model'].armour - w.armour_piercing:
                                            message.append("Armour fails!")
                                            if opossing_unit.take_damage(w.damage, []):
                                                stats[opfor]['KIA'] += 1
                                            if len(opossing_unit.models) == 0:
                                                message.append("\nUnit wiped out!")
                                                units[opfor].remove(opossing_unit)
                                        else:
                                            message.append("Armour saves!")
                                    else:
                                        message.append("Fails to wound")
                                else:
                                    message.append("Miss!")
                                print(", ".join(message))


def fight_phase(i, units, stats):
    opfor = get_opfor(i)
    # charge combats:
    for unit in units[i]:
        if unit.has_charged:
            print("Charging unit:")
            combat(i, units, unit, stats)
    # other combats (need to rank by importance metric threat, threatened)
    # alternates player
    for iu, ou in zip_longest(
        [u for u in units[i] if not unit.has_charged], units[opfor]):
        if iu:
            combat(i, units, iu, stats)
        if ou:
            combat(opfor, units, ou, stats)


def morale_test(i, units, stats):
    """Go through each unit and do test"""
    for unit in units[i]:
        unit_size = len(unit.models)
        loses = unit.models_lost
        if unit_size > 0 and loses > 0:
            leadership = max(m['model'].leadership for m in unit.models)
            morale_test = roll_d(6) + loses
            if morale_test > leadership:
                flee = min(max(morale_test - leadership, 0), unit_size)
                print("Morale Test Fails, {} models flee".format(flee))
                for x in range(flee):
                    model = unit.models.pop()
                    stats[i]['MIA'] += 1
                    print("{} flees".format(model['model'].name))
            else:
                print("Morale Test Passed!")


def morale_phase(i: int, units, stats):
    """Test both players starting with current player"""
    opfor = get_opfor(i)
    morale_test(i, units, stats)
    morale_test(opfor, units, stats)
