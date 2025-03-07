#!/usr/bin/python3
"""
This module starts a Flask web application
listening on 0.0.0.0, port 5000
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Returns 'Hello HBNB!' for the root URL"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns 'HBNB' for the URL '/hbnb'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Returns 'C ' followed by the value of the text variable"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python/',
           defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """Returns 'Python ' followed by
    the value of the text variable
    """
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Returns 'n is a number' only if n is an integer"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Displays an HTML page only if n is an integer"""
    return render_template('number_template.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """Displays an HTML page only if n is an integer,
    specifying if n is odd or even
    """
    parity = 'even' if n % 2 == 0 else 'odd'
    return render_template('6-number_odd_or_even.html',
                           n=n, parity=parity)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
