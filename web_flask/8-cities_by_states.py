#!/usr/bin/python3
"""Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    Display a HTML page with a list of all State and City objects
    in DBStorage, sorted by name (A->Z).
    """
    states = list(storage.all(State).values())
    sorted_states = sorted(states, key=lambda x: x.name)
    return render_template('8-cities_by_states.html',
                           states=sorted_states)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


if __name__ == '__main__':
    storage.reload()
    app.run('0.0.0.0', 5000)
