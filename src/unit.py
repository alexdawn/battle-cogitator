from collections import namedtuple
from enum import Enum
from typing import List, Tuple
import logging

import rules

Model = namedtuple(
    'Model', [
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


Power = namedtuple(
    'Power', ['name', 'power_level', 'ability']
)

Ability = namedtuple(
    'Ability', ['name', 'description', 'callback']
)


class Unit():
    def __init__(self, name: str, unit_type: str, pos: float, strategy: Enum, models: List[Model]):
        self.name = name
        self.unit_type = unit_type
        self.pos = pos
        self.strategy = strategy # hold|advance|charge|fallback
        self.moved = 'yet_to_move'
        self.has_charged = False
        self.models_lost = 0
        self.has_used_grenade = False
        self.models = models

    def reset(self):
        """Flags unit to start of the turn state"""
        self.moved = 'yet_to_move'
        self.has_charged = False
        self.models_lost = 0
        self.has_used_grenade = False

    def max_effective_range(self) -> float:
        """Find the maximum range of the unit"""
        return max(int(w.range) for m in self.models for w in m['weapons'] if w.range != 'melee')

    def unit_movement(self) -> float:
        """Finds the movement of the unit"""
        return min(m['model'].movement for m in self.models)

    def unit_toughness(self) -> float:  # not sure if to use toughest or least tough?
        """Find toughness to use for combats"""
        return max(m['model'].toughness for m in self.models)

    def take_damage(self, damage: int, message: List[str]) -> Tuple[bool, int]:
        """Apply damage to a model, return if the model is killed and how much damage was applied"""
        wounds_remaining = self.models[-1]['model'].wounds
        if damage >= wounds_remaining:
            self.models_lost += 1
            m = self.models.pop()
            message.append("{} is dead!".format(m['model'].name))
            return True, wounds_remaining
        else:
            p = self.models[-1]['model']
            self.models[-1]['model'] = p._replace(wounds = p.wounds - damage)
            message.append("{} is injured but not dead!".format(p['model'].name))
            return False, damage

    def hold(self):
        """Apply hold as a movement"""
        self.moved = 'held'
        logging.info("held at {}".format(self.pos))

    def move(self, distance, direction):
        """Move unit"""
        # need to check unit is not engaged
        assert distance <= self.unit_movement()
        self.moved = 'moved'
        self.pos += direction * distance
        logging.info("moved to {}".format(self.pos))

    def advance(self, distance, direction):
        """Advance unit with additional movement"""
        # check unit is not engaged
        assert distance <= self.unit_movement()
        self.moved = 'advanced'
        advance = rules.roll_d(6)
        logging.info("Advance an extra {}".format(advance))
        self.pos += (direction + advance) * distance
