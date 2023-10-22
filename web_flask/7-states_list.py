#!/usr/bin/python3
"""Minimal flask app"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display a HTML page with a list of
    all State objects in DBStorage.
    """
    states = list(storage.all(State).values())
    sorted_states = sorted(states, key=lambda x: x.name)
    return render_template('7-states_list.html',
                           states=sorted_states)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


if __name__ == '__main__':
    storage.reload()
    app.run(host='0.0.0.0', port=5000)
