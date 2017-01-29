#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask, g
from . import config
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(config)

# ######## session ##########

app.secret_key = app.config['SECRET_KEY']

# ######## logging ##########

formatter = logging.Formatter(app.config['LOG_FORMAT'])
handler = RotatingFileHandler(**app.config['LOG_HANDLER'])
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

#############################
