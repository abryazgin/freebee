#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Message:
    def __init__(self, id, time, text, sender):
        self.id = id
        self.sender = sender
        self.time = time
        self.text = text

    def __str__(self):
        return ('id = {0}, sender.login = {1}, ' +
                'time = {2}, text = {3}').format(
                self.id, self.sender.login,
                self.time, self.text)
