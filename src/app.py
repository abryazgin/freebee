#!/usr/bin/python3
# -*- coding:utf-8 -*-

from configurator import app
from request_parser import app_api
# from api import app_api

app.register_blueprint(app_api)


if __name__ == '__main__':
    app.run(debug=True)
