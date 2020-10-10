from rules import roll_d


# AH	Auto Hit
def auto_hit():
    def wrapper(phase, stats):
        if phase == 'aim':
            return True
    return wrapper


# AID	All is Dust (+1 to Saves if Damage is 1)
def all_is_dust():
    def wrapper(phase, stats):
        if phase == 'armour save' and stats['damage'] == 1:
            return
    return wrapper


# AW2	Always wounds on a 2+
def always_wound(amount: int = 2):
    def wrapper(phase, stats):
        if phase == 'wound':
            return roll_d(6) >= amount
    return wrapper


# D2	Additional 2 Damage on Wounds of 6
def extra_damage(amount: int = 2):
    def wrapper(phase, stats):
        if phase == 'wound':
            return
    return wrapper


# DR	Subtracts 1 from incoming Damage (to a minimum of 1)
def damage_reduction():
    def wrapper(phase, stats):
        if phase == 'damage':
            return
    return wrapper


# FNP5	5+ Feel No Pain, if armour save fails get a bonus save (apart from insta-death)
def feel_no_pain(amount: int = 5):
    def wrapper(phase, stats):
        if phase == 'armour save':
            return
    return wrapper


# INA	-1 to hit
def hit_penalty():
    def wrapper(phase, stats):
        if phase == 'aim':
            return
    return wrapper


# KNF	"They Shall Know No Fear" (reroll leadership)
def know_no_fear():
    def wrapper(phase, stats):
        if phase == 'morale':
            return
    return wrapper


# MD6	Melta D6 (roll two, take the highest)
def melta():
    def wrapper(phase, stats):
        if phase == 'damage':
            return
    return wrapper


# MW1	Additional Mortal Wound on 6 to Wound
# MWD3	Additional d3 Mortal Wounds on 6
def mortal_wound_on_wound(amount: str):
    def wrapper(phase, stats):
        if phase == 'wound':
            return
    return wrapper


# MW1H	Mortal wound on 6 to hit
def mortal_wound_on_hit():
    def wrapper(phase, stats):
        if phase == 'aim':
            return
    return wrapper


# MWD13	1 MW on 4+, d3 MW on 6+
def moral_wound_damage():
    def wrapper(phase, stats):
        if phase == 'wound':
            return
    return wrapper


# PSN	Wounds on 4+, except Vehicles and Titanic Units
def poison():
    def wrapper(phase, stats):
        if phase == 'wound':
            return
    return wrapper


# QS	Quantum Shielding (Ignores wounds on a dice roll higher than damage characteristic)
def quantum_shielding():
    def wrapper(phase, stats):
        if phase == 'wound':
            return
    return wrapper


# R3	-3 AP on 6
# R4	-4 AP on 6
def armour_pierce(amount: int):
    def wrapper(phase, stats):
        if phase == 'aim':
            return
    return wrapper


# RA4	4++ Against Ranged Attacks
# RA5	5++ against Ranged attacks
def invulnerable_save(amount: int):
    def wrapper(phase, stats):
        if phase == 'armour save':
            return
    return wrapper


# RR1	Rerolls 1's to hit
def reroll_ones():
    def wrapper(phase, stats):
        if phase == 'aim':
            return
    return wrapper


# RRW	Rerolls Wounds
def reroll_wounds():
    def wrapper(phase, stats):
        if phase == 'wound':
            return
    return wrapper
