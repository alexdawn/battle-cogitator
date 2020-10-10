from flask import Flask, jsonify

from simulation import simulate_games
from thoughts import thought_for_the_day
from names import generate_name
from date import get_imperial_date_now

app = Flask(__name__)


@app.route('/api/simulate')
def index():
    # data = request.get_json()
    data = {  # noqa: F841
        'game_settings': {
            'max_turns': 0,  # zero unlimited rounds
            'simulation_mode': {
                'mode': 'monte_carlo',  # monte_carlo | markov
                'sample_size': 10,
            },
            'calculate_first_bias': True,
            'strategy': 'heuristics',  # heuristics | ai
            'unit_shape': 'point',  # point | area | individuals
            'map': {
                'light_cover': 0,
                'heavy_cover': 0,
                'obscuring': 0
            },
            'board_length': 60,
            'board_width': None
        },
        'players': [
            {
                'name': 'loyalists',
                'faction': 'imperial',
                'units': [
                    {
                        'name': '1st Squad',
                        'position': 0,
                        'orders': 'advance',
                        'models': [
                            {
                                'profile': ['guy', 6, 4, 4, 4, 4, 1, 1, 8, 5],
                                'weapons': [
                                    ['laspistol', 18, 'pistol 1', 4, 0, 1, None],
                                    ['grenade', 8, 'grenade D3', 8, -1, 1, None],
                                    ['chainsword', 'melee', 'melee 2', 5, -1, 1, None]
                                ],
                                'abilities': [],
                                'powers': []
                            }
                        ]
                    }
                ]
            },
            {
                'name': 'Traitors',
                'faction': 'chaos',
                'units': [
                    {
                        'name': '1st Squad',
                        'position': 50,
                        'orders': 'advance',
                        'models': [
                            {
                                'profile': ['baz', 6, 4, 4, 4, 4, 1, 1, 8, 5],
                                'weapons': [
                                    ['laspistol', 18, 'pistol 1', 4, 0, 1, None],
                                    ['grenade', 8, 'grenade D3', 8, -1, 1, None],
                                    ['chainsword', 'melee', 'melee 2', 5, -1, 1, None]
                                ],
                                'abilities': [],
                                'powers': []
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return jsonify({**simulate_games(10), "date": get_imperial_date_now()})


@app.route('/api/performance')
def performance():
    return jsonify({'stats': []})


@app.route('/api/thought')
def thought():
    return jsonify({
        "date": get_imperial_date_now(),
        'thought': thought_for_the_day()})


@app.route('/api/name')
def name():
    return jsonify({'names': [generate_name() for x in range(10)]})


@app.route('/api/date')
def date():
    return jsonify({'current_date': get_imperial_date_now()})


app.run(debug=True)
