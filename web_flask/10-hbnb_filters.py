#!/usr/bin/python3
"""Flask web application"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity

app = Flask(__name__)
app.static_folder = 'web_flask/static'
app.template_folder = 'web_flask/templates'


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Display a HTML page with filters for States,
    Cities, and Amenities.
    """
    states = list(storage.all(State).values())
    sorted_states = sorted(states, key=lambda x: x.name)

    cities = list(storage.all(City).values())
    sorted_cities = sorted(cities, key=lambda x: x.name)

    amenities = list(storage.all(Amenity).values())
    sorted_amenities = sorted(amenities, key=lambda x: x.name)

    return render_template('10-hbnb_filters.html',
                           states=sorted_states,
                           cities=sorted_cities,
                           amenities=sorted_amenities)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


if __name__ == '__main__':
    storage.reload()
    app.run(host='0.0.0.0', port=5000)
