from random import randrange
from typing import Tuple, List, Dict, Any
from itertools import zip_longest
from math import ceil
import logging
from typing import Optional

from unit import Unit, Model, Weapon, MoveStatus
from powers import psychic_test
from stratgey import Strategy, get_strategy_function


def take_round(players: List[str], units: List[List[Unit]], stats: List[Dict[str, Any]], options)\
        -> bool:
    """Play a round for each player"""
    for i, p in enumerate(players):
        for x, name in enumerate(players):
            for unit in units[x]:  # reset states
                unit.reset()
                if get_seperation(unit, get_nearest_opposing_unit(unit, get_opfor(x), units)) > 1:
                    unit.engaged = False

        won = take_turn(i, p, units, stats, options)
        if won:
            break
    return won


def player_model_count(units: List[List[Unit]], i: int) -> int:
    """Get count of models player has"""
    return sum(len(u.models) for u in units[i])


def player_has_models(units: List[List[Unit]], i: int) -> bool:
    """Does player have any models left?"""
    return player_model_count(units, i) > 0


def take_turn(i: int, player: str, units: List[List[Unit]], stats: List[Dict[str, Any]], options)\
        -> bool:
    """Run through each phase"""
    logging.info("{}".format(player))
    logging.info("====")
    command_phase(i, units)
    move_phase(i, units)
    reinforcement_phase(i, units, options)
    psychic_phase(i, units, stats)
    shooting_phase(i, units, stats)
    charge_phase(i, units, stats)
    fight_phase(i, units, stats)
    morale_phase(i, units, stats)
    return not player_has_models(units, 0) or not player_has_models(units, 1)


def roll_d(x: int) -> int:
    """Roll a DX"""
    return randrange(1, x)


MODIFIER_ORDER = {
    '/': 1,
    '*': 2,
    '+': 3,
    '-': 4
}


def apply_modifier(result: float, modifier: Tuple[str, int]) -> float:
    """Apply modifier for dice roll"""
    if modifier[0] == '+':
        return result + modifier[1]
    elif modifier[0] == '-':
        return result - modifier[1]
    elif modifier[0] == '*':
        return result * modifier[1]
    elif modifier[0] == '/':
        return result / modifier[1]
    else:
        raise RuntimeError("Unknown operator {}".format(modifier[0]))


def apply_modifiers(x: str, modifiers: List[Tuple[str, int]]) -> str:
    if x == '-':
        return '-'
    result = float(x)
    for mod in sorted(modifiers, key=lambda mod: MODIFIER_ORDER[mod[0]]):
        result = apply_modifier(result, mod)
    return str(ceil(result))


def maximum_modification(x: str, modifiers: List[Tuple[str, int]], clamp_value: int) -> str:
    """Clamps the modifier to not change more than +/- the clamp value"""
    return str(max(min(
        int(apply_modifiers(x, modifiers)), int(x) + clamp_value), int(x) - clamp_value))


def get_seperation(unit1: Unit, unit2: Optional[Unit]) -> float:
    """Get Distance between two units"""
    if type(unit2) == Unit:
        return float(unit2.pos - unit1.pos)  # type: ignore
    else:
        return float("inf")


def get_units_within(i: int, unit: Unit, units: List[List[Unit]], max_dist: float) -> List[Unit]:
    """Get units"""
    return [
        x for x in sorted(units[i], key=lambda ou: get_seperation(unit, ou))
        if get_seperation(unit, x) <= max_dist]


def get_nearest_opposing_unit(unit: Unit, opfor: int, units: List[List[Unit]]) -> Optional[Unit]:
    """Find the nearest opposing unit"""
    opossed = get_units_within(opfor, unit, units, float("inf"))
    if opossed:
        return opossed[0]
    return None


def get_opfor(i: int) -> int:
    """Get the player index for the opposition player"""
    return 1 if i == 0 else 0


def command_phase(i: int, units: List[List[Unit]]) -> None:
    """Add Command Points, apply tactics"""
    logging.warning("No Command Points yet!")
    # if player[i].is_battle_forged:
    #     player[i].command_points += 1


def move_phase(i: int, units: List[List[Unit]]) -> None:
    """Move a players models"""
    for unit in units[i]:
        if unit.models:
            opossing_unit = get_nearest_opposing_unit(unit, get_opfor(i), units)
            seperation = get_seperation(unit, opossing_unit)
            direction = 1 if seperation > 0 else -1
            strat = get_strategy_function(unit.strategy)
            strat(unit, abs(seperation), direction)


def reinforcement_phase(i: int, units: List[List[Unit]], options) -> None:
    """Add units that arrive to the board late"""
    for unit in units[i]:
        if unit.off_board:  # No idea if there is restrictions in which round it can join or where?
            unit.add_to_board(options['reinforce_position_{}'.format(i)])


def psychic_phase(i: int, units: List[List[Unit]], stats) -> None:
    """Cast psychic powers"""
    cast_powers = set()
    for unit in units[i]:
        for u, m in enumerate(unit.models):
            for power in m.powers:
                if power not in cast_powers:  # cannot reuse the same power in a phase
                    if power.name != 'smite':  # smite can be cast unlimited times by units
                        cast_powers.add(power)
                    opossing_unit = get_nearest_opposing_unit(unit, get_opfor(i), units)
                    if opossing_unit:  # TODO handle powers which do not target an opponent
                        psychic_test(unit, power, opossing_unit, units)
                    break  # unit can only use one power


def wound_roll(strength: int, toughness: int) -> Tuple[int, bool]:
    """Use the wound chart, then do a wound roll"""
    result = roll_d(6)
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
    return result, result >= need


def choose_weapon(unit: Unit, seperation: float, weapons: List[Weapon]) -> List[Weapon]:
    """choose non-pistol if option, model with weakest wepaon the grenade"""
    if abs(seperation) <= 1:
        if unit.has_big_guns_never_tire():
            return [w for w in weapons if w.ability != 'blast']
        else:
            return [w for w in weapons if "pistol" in w.type]
    else:
        if not unit.has_used_grenade and len(
                [w for w in weapons if "grenade" in w.type and w.range < seperation]):
            unit.has_used_grenade = True
            return [w for w in weapons if "grenade" in w.type]  # TODO pick one sort of grenade
        else:  # TODO handle when one weapon has weapon profiles?
            return [w for w in weapons if "pistol" not in w.type and "grenade" not in w.type]


def can_attack(unit: Unit, seperation: float, weapon: Weapon) -> bool:
    """Check movement to see if weapon type can attack"""
    weapon_type, _ = weapon.type.split(" ")
    engagement_block = unit.engaged and not unit.has_big_guns_never_tire()
    if unit.engaged and weapon.ability == 'blast':  # blast weapons can never attack in engagement
        return False
    if unit.moved == 'advanced' and weapon_type == 'assault' and not engagement_block:
        return True
    elif unit.moved != 'advanced' and not engagement_block:
        return True
    elif unit.moved != 'advanced' and weapon_type == 'pistol':
        return True
    else:
        return False


def aim_penalty(unit: Unit, weapon_type: str) -> List[Tuple[str, int]]:
    """Check movement to see if there are aim penalties"""
    penalties = []
    if unit.moved == 'advanced' and weapon_type == 'assault':
        penalties.append(('-', 1))
    if unit.moved != MoveStatus.HELD and weapon_type == 'heavy':
        penalties.append(('-', 1))
    if unit.engaged and weapon_type == 'heavy':
        assert unit.has_big_guns_never_tire(), "Only vehicles and monster can shoot while engaged"
        penalties.append(('-', 1))
    return penalties


def resolve_die_notation(text: str) -> Tuple[int, int]:
    """Resolve variable attacks notation, value and max value (used for blast weapons)"""
    if 'D' in text:
        if 'D3':
            return roll_d(3), 3
        elif '2D3':
            return roll_d(3) + roll_d(3), 6
        elif 'D6':
            return roll_d(6), 6
        elif '2D6':
            return roll_d(6) + roll_d(6), 12
        elif '3D6':
            return roll_d(6) + roll_d(6) + roll_d(6), 18
        elif '4D6':
            return roll_d(6) + roll_d(6) + roll_d(6) + roll_d(6), 24
        elif 'D3+ 3':
            return roll_d(3) + 3, 6
        elif 'D6+3':
            return roll_d(6) + 3, 9
        elif 'D6MIN3':
            return min(roll_d(6), 3), 6
        else:
            raise RuntimeError("Unknown Die format {}".format(text))
    else:
        return int(text), int(text)


def flavour_text(name: str, weapon_type: str) -> str:
    texts = {
        'rapid_fire': 'double taps with',
        'assault': 'sprays with',
        'heavy': 'blasts with',
        'grenade': 'lobs',
        'pistol': 'draws and fires',
        'melee': 'hits with'
    }
    return (texts[weapon_type] +
            (" an " if name[0].lower() in ('a', 'e', 'i', 'o', 'u') else " a ") +
            name)


def aim(
        i: int, model: Model, unit: Unit, weapon: Weapon,
        opossing_unit: Unit, is_overwatch: bool, combat_log: List[str], stats) -> bool:
    """Part of attacking see if weapon hits"""
    result = roll_d(6)
    if weapon.type.split(" ")[0] != 'melee':
        success = result > 1 and result >= (
            6 if is_overwatch
            else int(maximum_modification(
                model.model.ballistic_skill,
                aim_penalty(unit, weapon.type.split(" ")[0]),
                1
            ))
        )
    else:
        success = result > 1 and result >= model.model.weapon_skill
    combat_log.append(
        "{} {}".format(
            model.model.name,
            flavour_text(weapon.name, weapon.type.split(" ")[0])
        )
    )
    if success:
        combat_log.append("Hit!")
        return wound(i, unit, weapon, opossing_unit, combat_log, stats)
    else:
        combat_log.append("Miss!")
        return False


def wound(i: int, unit: Unit, weapon: Weapon, opossing_unit: Unit, combat_log: List[str], stats)\
        -> bool:
    """Roll to see if hit causes a wound"""
    result, success = wound_roll(weapon.strength, opossing_unit.unit_toughness())
    if success:
        combat_log.append("Wounds!")
        return armour_save(i, unit, weapon, opossing_unit, combat_log, stats)
    else:
        combat_log.append("Fails to wound")
        return False


def armour_save(
        i: int, unit: Unit, weapon: Weapon, opossing_unit: Unit, combat_log: List[str], stats)\
        -> bool:
    """Roll ot see if armour saves"""
    # TODO handle invurable saves
    result = roll_d(6)
    success = result < opossing_unit.models[-1].model.armour - weapon.armour_piercing
    if success:
        combat_log.append("Armour fails!")
        return damage(i, unit, weapon, opossing_unit, combat_log, stats)
    else:
        combat_log.append("Armour saves!")
        return False


def damage(i: int, unit: Unit, weapon: Weapon, opossing_unit: Unit, combat_log: List[str], stats)\
        -> bool:
    """Work out and apply damage"""
    opfor = get_opfor(i)
    damage, _ = resolve_die_notation(weapon.damage)
    model_died, damage_inflicted = opossing_unit.take_damage(damage, combat_log)
    if model_died:
        stats[opfor]['KIA'] += 1
        stats[opfor]['killzone'].extend([opossing_unit.pos])
        stats[i]['overkill'].extend([int(damage - damage_inflicted)])
    if damage_inflicted:
        stats[i]['damage_per_unit'][unit.name] += damage_inflicted
        stats[i]['damage_per_weapon'][weapon.name] += damage_inflicted
    return True


def shoot_with_unit(
        i: int, units: List[List[Unit]], unit: Unit, stats: List[Dict[str, Any]],
        is_overwatch: bool = False, charging_unit: Unit = None)\
        -> None:
    """Do shots with a unit"""
    # TODO handle grenade to be thrown by model with worst weapons
    # TODO look out sir
    opfor = get_opfor(i)
    if len(units[opfor]):
        opossing_unit = charging_unit if is_overwatch else get_nearest_opposing_unit(
            unit, opfor, units)
        sep = get_seperation(unit, opossing_unit)
        # sorts attacks by target then weapon
        attacks = sorted(
            [(m, w) for m in unit.models for w in choose_weapon(unit, sep, m.weapons)],
            key=lambda x: x[1].name
        )
        for m, w in attacks:
            weapon_type, attack_notation = w.type.split(" ")
            number_of_attacks, max_attacks = resolve_die_notation(attack_notation)
            if w.ability == 'blast':  # blast attacks have special rules for large units
                if opossing_unit and len(opossing_unit.models) > 10:
                    number_of_attacks = max_attacks
                elif opossing_unit and len(opossing_unit.models) > 5:
                    number_of_attacks = max(number_of_attacks, 3)

            if weapon_type == 'rapid_fire' and abs(sep) <= w.range / 2:
                logging.info("Rapid fire weapon is at close range, twice the attacks")
                number_of_attacks *= 2

            if (w.range != 'melee' and
                    (weapon_type != 'grenade' or not unit.has_used_grenade) and
                    can_attack(unit, abs(sep), w) and
                    abs(sep) <= w.range):
                for a in range(int(number_of_attacks)):
                    if opossing_unit and len(opossing_unit.models) > 0:
                        combat_log: List[str] = []
                        aim(i, m, unit, w, opossing_unit, is_overwatch, combat_log, stats)
                        if len(opossing_unit.models) == 0:
                            combat_log.append("Unit wiped out!")
                            units[opfor].remove(opossing_unit)
                        logging.info(" ".join(combat_log))


def shooting_phase(i: int, units: List[List[Unit]], stats: List[Dict[str, Any]]) -> None:
    """Shoot with each unit in turn"""
    for unit in units[i]:
        if unit.can_attack():
            shoot_with_unit(i, units, unit, stats)


def charge_phase(i: int, units: List[List[Unit]], stats: List[Dict[str, Any]]) -> None:
    """Do charge phase"""
    opfor = get_opfor(i)
    direction = 1 if i == 0 else -1
    for unit in units[i]:
        if unit.models and unit.strategy in (Strategy.CHARGE, Strategy.HCHARGE):
            opossing_unit = get_nearest_opposing_unit(unit, get_opfor(i), units)
            if opossing_unit:
                seperation = abs(get_seperation(unit, opossing_unit))
                if units[i] and seperation <= 12 and seperation > 1:
                    if not opossing_unit.engaged:
                        logging.info("Defender fires in overwatch...")
                        shoot_with_unit(
                            opfor, units, opossing_unit, stats,
                            is_overwatch=True, charging_unit=unit
                        )
                    charge = roll_d(6) + roll_d(6)
                    if charge >= seperation:
                        logging.info("Charge success {}".format(charge))
                        unit.engaged, opossing_unit.engaged = True, True
                        unit.pos += direction * min(charge, seperation)
                        # TODO do heroic interventions
                    else:
                        logging.info("Charge failed rolled {}, but needed {}".format(
                            charge, seperation))


def combat(i: int, units: List[List[Unit]], unit: Unit, stats: List[Dict[str, Any]]) -> None:
    """Enact the combat for one unit"""
    opfor = get_opfor(i)
    if len(units[opfor]):
        opossing_unit = get_nearest_opposing_unit(unit, opfor, units)
        sep = get_seperation(unit, opossing_unit)
        if abs(sep) <= 1 and opossing_unit:
            for u, m in enumerate(unit.models):
                for w in m.weapons:
                    weapon_type, attacks = w.type.split(" ")
                    if w.range == 'melee':
                        for a in range(int(attacks)):
                            if len(opossing_unit.models):
                                combat_log: List[str] = []
                                aim(i, m, unit, w, opossing_unit, False, combat_log, stats)
                                if len(opossing_unit.models) == 0:
                                    combat_log.append("Unit wiped out!")
                                    unit.engaged, opossing_unit.engaged = False, False
                                    units[opfor].remove(opossing_unit)
                                logging.info(" ".join(combat_log))


def fight_phase(i: int, units: List[List[Unit]], stats: List[Dict[str, Any]]) -> None:
    """Fight phase rules, do charging combats first, then alternate other combats"""
    opfor = get_opfor(i)
    # charging unit fight first
    for unit in units[i]:
        if unit.has_charged:
            logging.info("Charging unit:")
            combat(i, units, unit, stats)
    # other combats go next, alternating players
    # # TODO  need to rank by importance metric threat, threatened
    for iu, ou in zip_longest(
            [u for u in units[i] if not unit.has_charged], units[opfor]):
        if iu:
            combat(i, units, iu, stats)
        if ou:
            combat(opfor, units, ou, stats)


def morale_test(i: int, units: List[List[Unit]], stats: List[Dict[str, Any]]) -> None:
    """Go through each unit and do morale test"""
    for unit in units[i]:
        unit_size = len(unit.models)
        if unit_size > 0 and unit.models_lost > 0:
            leadership = unit.unit_leadership()
            result = roll_d(6)
            morale_result = result + unit.models_lost
            if result > 1 and morale_result > leadership:
                flee = 1
                modifier = -1 if unit_size < unit.starting_strength / 2 else 0
                for x in range(unit_size - 1):
                    if roll_d(6) + modifier <= 1:
                        flee += 1
                logging.info("Morale Test Fails, {} models flee".format(flee))
                for x in range(flee):
                    model = unit.models.pop()
                    stats[i]['MIA'] += 1
                    logging.info("{} flees".format(model.model.name))
            else:
                logging.info("{} passes Morale Test!".format(unit.name))


def morale_phase(i: int, units: List[List[Unit]], stats: List[Dict[str, Any]]) -> None:
    """Test both players starting with current player"""
    opfor = get_opfor(i)
    # TODO technically should alternate player, not that it should make a difference here?
    morale_test(i, units, stats)
    morale_test(opfor, units, stats)
    # Coherencey Test not needed for point units
