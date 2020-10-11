from collections import namedtuple
from enum import Enum
from typing import List, Tuple
import logging

import rules

ModelStats = namedtuple(
    'ModelStats', [
        'name', 'movement', 'weapon_skill', 'ballistic_skill',
        'strength', 'toughness', 'wounds', 'attacks', 'leadership', 'armour'])

Weapon = namedtuple(
    'Weapon', [
        'name', 'range', 'type',
        'strength', 'armour_piercing', 'damage', 'ability'])


class WeaponType(Enum):
    RAPID_FIRE = 1
    ASSAULT = 2
    HEAVY = 3
    GRENADE = 4
    PISTOL = 5
    MELEE = 6


class MoveStatus(Enum):
    YET_TO_MOVED = 1
    HELD = 2
    MOVED = 3
    ADVANCED = 4
    FELL_BACK = 5


Power = namedtuple(
    'Power', ['name', 'power_level', 'ability']
)

Ability = namedtuple(
    'Ability', ['name', 'description', 'callback']
)

DamageTable = namedtuple(
    'DamageTable', ['min', 'max', 'stats']
)


class Model():
    def __init__(
            self, model: ModelStats, damage_table: List[DamageTable], powers: List[Power],
            abilities: List[Ability], weapons: List[Weapon]):
        self.model = model
        self.damage_table = damage_table
        self.powers = powers
        self.abilities = abilities
        self.weapons = weapons

    def apply_damage(self, damage: int):
        if damage < self.model.wounds:
            self.model = self.model._replace(wounds=self.model.wounds - damage)
            self.update_stats()

    def update_stats(self):
        for row in self.damage_table:
            if self.model.wounds <= row.max and self.model.wounds >= row.min:
                for x in row.stats:
                    pass
                break


class Unit():
    def __init__(self, name: str, unit_type: str, pos: float,
                 strategy, models: List[Model]):
        self.name = name
        self.unit_type = unit_type
        self.pos = pos
        self.strategy = strategy  # Type Enum
        self.moved = MoveStatus.YET_TO_MOVED  # Tyoe: MoveStatus
        self.has_charged = False
        self.engaged = False
        self.models_lost = 0
        self.starting_strength = len(models)
        self.has_used_grenade = False
        self.models = models

    def reset(self):
        """Flags unit to start of the turn state"""
        self.moved = MoveStatus.YET_TO_MOVED
        self.has_charged = False
        self.models_lost = 0
        self.has_used_grenade = False

    def max_effective_range(self) -> float:
        """Find the maximum range of the unit"""
        return max(int(w.range) for m in self.models for w in m.weapons if w.range != 'melee')

    def unit_movement(self) -> float:
        """Finds the movement of the unit"""
        return float(min(m.model.movement for m in self.models))

    def unit_toughness(self) -> int:
        """Find toughness to use for combats"""
        return int(self.models[-1].model.toughness)

    def unit_leadership(self) -> int:
        """Get the maximum leadership of unit"""
        return int(max(m.model.leadership for m in self.models))

    def is_within(self, pos: float, distance: float) -> bool:
        """Check if unit is within distance of a position"""
        return abs(self.pos - pos) < distance

    def take_damage(self, damage: int, message: List[str]) -> Tuple[bool, int]:
        """Apply damage to a model, return if the model is killed and how much damage was applied"""
        wounds_remaining = self.models[-1].model.wounds
        if damage >= wounds_remaining:
            self.models_lost += 1
            m = self.models.pop()
            message.append("{} is dead!".format(m.model.name))
            return True, wounds_remaining
        else:
            p = self.models[-1].model
            self.models[-1].model = p._replace(wounds=p.wounds - damage)
            message.append("{} is injured but not dead!".format(p.name))
            return False, damage

    def hold(self):
        """Apply hold as a movement"""
        self.moved = MoveStatus.HELD
        logging.info("held at {}".format(self.pos))

    def move(self, distance, direction):
        """Move unit"""
        if not self.engaged:
            assert distance <= self.unit_movement()
            self.moved = MoveStatus.MOVED
            self.pos += direction * distance
            logging.info("moved to {}".format(self.pos))
        else:
            raise RuntimeError("Ordered to move but engaged")

    def advance(self, distance, direction):
        """Advance unit with additional movement"""
        if not self.engaged:
            assert distance <= self.unit_movement()
            self.moved = MoveStatus.ADVANCED
            advance = rules.roll_d(6)
            logging.info("Advance an extra {}".format(advance))
            self.pos += (distance + advance) * direction
        else:
            raise RuntimeError("Ordered to advance but engaged")

    def fall_back(self, distance, direction):
        """Fall back and be unable to shoot etc..."""
        if self.engaged:
            assert distance <= self.unit_movement()
            self.moved = MoveStatus.FELL_BACK
            logging.info("Unit fell back")
            self.pos += distance * -direction
            self.engaged = False
        else:
            raise RuntimeError("Ordered to fall back but not engaged")
