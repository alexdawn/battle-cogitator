from enum import Enum


class Strategy(Enum):
    HOLD = 1
    ADVANCE = 2
    CHARGE = 3
    HCHARGE = 4
    DISTANCE = 5


def get_strategy_function(strategy):
    options = {
        Strategy.HOLD: hold,
        Strategy.ADVANCE: slow_advance,
        Strategy.CHARGE: charge,
        Strategy.HCHARGE: headlong_charge,
        Strategy.DISTANCE: keep_seperation,
    }
    return options[strategy]


def hold(unit, seperation, direction):
    return unit.hold()


def slow_advance(unit, seperation, direction):
    if seperation > unit.max_effective_range():
        unit.move(unit.unit_movement(), direction)
    else:
        unit.hold()


def charge(unit, seperation, direction):
    if seperation > 12 + unit.unit_movement():
        unit.move(unit.unit_movement(), direction)
    elif seperation > 1:
        unit.move(min(unit.unit_movement(), seperation - 1), direction)
    else:
        unit.hold()


def headlong_charge(unit, seperation, direction):
    if seperation > 12 + unit.unit_movement():
        unit.advance(unit.unit_movement(), direction)
    elif seperation > 1:
        unit.move(min(unit.unit_movement(), seperation - 1), direction)
    else:
        unit.hold()


def keep_seperation(unit, seperation, direction):
    if seperation < unit.max_effective_range():
        unit.move(min(unit.unit_movement(), unit.max_effective_range() - seperation), -direction)
    else:
        unit.hold()
