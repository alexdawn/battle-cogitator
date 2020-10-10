import random
# TODO theme them on topic

thoughts = [
    'Only fools fail in their duties',
    'Negotitation is surender',
    'A mind without purpose will wander in dark places',
    'Analysis is the bane of conviction',
    'Look upon the Emperor\'s works and tremble',
    'Knowledge is to be feared!',
    'Victory is the promise of the emperor\'s command',
    'We are certain only of death',
]


def thought_for_the_day():
    return "Thought for the day: {}".format(random.choice(thoughts))
