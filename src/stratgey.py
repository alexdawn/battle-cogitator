from typing import Callable
from enum import Enum

from unit import Unit


class Strategy(Enum):
    HOLD = 1
    ADVANCE = 2
    CHARGE = 3
    HCHARGE = 4
    DISTANCE = 5


def get_strategy_function(strategy: Strategy) -> Callable[[Unit, float, float], None]:
    options = {
        Strategy.HOLD: hold,
        Strategy.ADVANCE: slow_advance,
        Strategy.CHARGE: charge,
        Strategy.HCHARGE: headlong_charge,
        Strategy.DISTANCE: keep_seperation,
    }
    return options[strategy]


def hold(unit: Unit, seperation: float, direction: float) -> None:
    """This unit will never move"""
    unit.hold()


def slow_advance(unit: Unit, seperation: float, direction: float) -> None:
    """This unit will move into range and hold"""
    if seperation > unit.max_effective_range():
        unit.move(
            min(unit.unit_movement(), seperation - unit.max_effective_range()),
            direction
        )
    else:
        unit.hold()


def charge(unit: Unit, seperation: float, direction: float) -> None:
    """This unit will move, shoot and attempt to charge when in range"""
    if seperation > 12 + unit.unit_movement():
        unit.move(unit.unit_movement(), direction)
    elif seperation > 1:
        unit.move(min(unit.unit_movement(), seperation - 1), direction)
    else:
        unit.hold()


def headlong_charge(unit: Unit, seperation: float, direction: float) -> None:
    """This unit will move as fast as it can, then charge"""
    if seperation > 12 + unit.unit_movement():
        unit.advance(unit.unit_movement(), direction)
    elif seperation > 1:
        unit.move(min(unit.unit_movement(), seperation - 1), direction)
    else:
        unit.hold()


def keep_seperation(unit: Unit, seperation: float, direction: float) -> None:
    """This unit will actively try and keep its range from enemies"""
    if unit.engaged:
        unit.fall_back(unit.unit_movement(), -direction)
    elif seperation < unit.max_effective_range():
        unit.move(min(unit.unit_movement(), unit.max_effective_range() - seperation), -direction)
    else:
        unit.hold()
