import random

cadian_names = [
    'Jens',
    'Karsk',
    'Hekler',
    'Reeve',
    'Pavlo',
    'Hektor',
    'Nils',
    'Thenmann',
    'Kyser',
    'Erlen',
    'Raphe',
    'Creed',
    'Lasko',
    'Ackerman',
    'Mattias',
    'Mortens',
    'Dansk',
    'Feodor',
    'Tomas',
    'Kolson',
    'Vance',
    'Pask',
    'Niems',
    'Gryf',
    'Willem',
    'Sonnen',
    'Ekhter',
    'Farestein',
    'Dekker',
    'Graf',
    'Arvans',
    'Viers',
    'Kolm',
    'Bask',
    'Vesker',
    'Palvo'
]


def generate_name():
    return "{}".format(random.choice(cadian_names))
