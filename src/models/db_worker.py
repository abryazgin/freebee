#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
# import mylogging


def _execute(conn, sql_query, sql_args=None):
    # mylogging.write(sql_query)
    # return [rows.fetchall() for rows in conn.execute(sql_query, sql_args, multi=True) if rows.with_rows]
    return conn.execute(sql_query, sql_args, multi=True)


def execute(conn, sql_query, sql_args=None):
    """
    Для SELECT и INSERT
    Возвращает результат SELECT либо LAST_INSERT_ID()
    """
    executed = _execute(conn, sql_query, sql_args)
    results = [rows.fetchall() for rows in executed if rows.with_rows]
    return results[len(results) - 1]


def change(conn, sql_query, sql_args=None):
    """
    Для DELETE и UPDATE
    Возвращает количество изменённых записей.
    """
    executed = _execute(conn, sql_query, sql_args)
    for result in executed:
        if not result.with_rows:
            return result.rowcount


def get_db():
    db = mysql.connector.connect(host='localhost',
                                 user='freebee',
                                 passwd='221uml?Po',
                                 db='freebee',
                                 charset='utf8')
    return db
