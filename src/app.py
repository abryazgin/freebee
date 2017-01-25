#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask, g
from .api import app_api
from . import config
# from .models.db_worker import get_db

app = Flask(__name__)
app.config.from_object(config)
# app.secret_key =
app.register_blueprint(app_api)


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
