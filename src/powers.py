from typing import TYPE_CHECKING, List
import logging

import rules

if TYPE_CHECKING:
    from unit import Unit, Power


def psychic_test(caster: 'Unit', power: 'Power', target_unit: 'Unit', units: 'List[List[Unit]]')\
        -> None:
    """Test to see if power can be manifest"""
    result = rules.roll_d(6) + rules.roll_d(6)
    if result in (2, 12):
        perils_of_the_warp(caster, units)
    if result >= power.warp_charge:
        if not deny_the_witch(result):
            power.ability(result, target_unit)
        else:
            logging.info("Denied {}".format(power.name))


def smite(result: int, target_unit: 'Unit') -> None:
    """Basic power known by all psykers"""
    if result > 10:
        wounds = rules.roll_d(6)
    else:
        wounds = rules.roll_d(3)
    # need method to apply mortal wounds without wasted damage
    target_unit.take_damage(wounds, [])


def deny_the_witch(result: int) -> bool:
    """Check to see if oponent can stop power"""
    return rules.roll_d(6) + rules.roll_d(6) > result


def perils_of_the_warp(caster: 'Unit', units: 'List[List[Unit]]') -> None:
    """Oh no the eldrich horror!"""
    wounds = rules.roll_d(3)
    killed = caster.take_damage(wounds, [])
    if killed:
        for unit in (
                rules.get_units_within(0, caster, units, 6) +
                rules.get_units_within(1, caster, units, 6)):
            unit.take_damage(rules.roll_d(3), [])
