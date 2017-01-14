#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
import logging


def _execute(conn, sql_query, sql_args=None):
    # logging.write(sql_query)
    return [rows.fetchall() for rows in conn.execute(sql_query, sql_args, multi=True) if rows.with_rows]


def execute(conn, sql_query, sql_args=None):
    results = _execute(conn, sql_query, sql_args)
    return results[len(results) - 1]


def get_db():
    db = mysql.connector.connect(host='localhost',
                                 user='freebee',
                                 passwd='221uml?Po',
                                 db='freebee',
                                 charset='utf8')
    return db
