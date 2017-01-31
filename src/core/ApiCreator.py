#!/usr/bin/python3
# -*- coding:utf-8 -*-


class ApiCreator(object):

    def __init__(self, app):
        self._app = app

    def get_api_from_actoin(self, action_method):
        self._app.add_url_rule()