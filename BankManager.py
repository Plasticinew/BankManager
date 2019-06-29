import os
import sqlite3
import sqlalchemy
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# def connect_db():
#     """Connects to the specific database."""
#     # rv = sqlite3.connect(app.config['DATABASE'])
#     # rv.row_factory = sqlite3.Row
#     rv = engine.connect()
#     return rv


if __name__ == '__main__':
    app.run()