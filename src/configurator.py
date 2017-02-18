#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask
import config
import logging
from core.logging import GzRotatingFileHandler


app = Flask(__name__)
app.config.from_object(config)

# ######## session ##########

app.secret_key = app.config['SECRET_KEY']

# ######## logging ##########

formatter = logging.Formatter(app.config['LOG_FORMAT'])
handler_conf = app.config['LOG_HANDLER']
handler = GzRotatingFileHandler(**handler_conf)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

#############################
