import mysql.connector
from contextlib import contextmanager

import config as config


class DBException(Exception):
    pass


class SqlResult:
    """
    Представляет результат запроса к бд.
    """
    def __init__(self, result, rescode, rowcnt, errormsg):
        """
        :param result: содержит результат последнего SELECT в процедуре SQL
        :param rescode: 1 - для процедур, завершившихся успешно;
                        0 - для процедур, в которые переданы некорректные
                            параметры;
                        None - для процедур, осуществляющих чтение из бд
        :param rowcnt: кол-во изменённых строк
        :param errormsg: если rescode = 0, представляет сообщение
                         об ошибке в процедуре SQL
        """
        self.result = result
        self.rescode = rescode
        self.rowcnt = rowcnt
        self.errormsg = errormsg


def _execute(conn, sql_query, sql_args=None):
    """
    Выполняет запрос к бд. Не для внешнего использования.
    :param conn: объект mysql.connector.connect.cursor()
    """
    return conn.execute(sql_query, sql_args, multi=True)


def execute(conn, sql_query, sql_args=None):
    """
    Выполняет запрос к бд и предоставляет результат
    в форме экземпляра SqlResult.

    Не для внешнего использования.
    :param conn: объект mysql.connector.connect
    """
    executed = _execute(conn, sql_query, sql_args)

    # вытаскиваем последний SELECT в процедуре
    results = [rows.fetchall() for rows in executed if rows.with_rows]
    result = results[len(results) - 1]
    # смотрим код результат (1 - успешно, 0 - была ошибка)
    # если вид запроса - SELECT, rescode =  None
    rescode = result[0].get('RESCODE', None) if result else None
    # смотрим сообщение об ошибке
    errormsg = result[0].get('MSG', None) if result else None

    # вытаскиваем кол-во изменённых строк
    rowcnts = [rows.rowcount for rows in executed if not rows.with_rows]
    rowcnt = rowcnts[len(rowcnts) - 1] if len(rowcnts) != 0 else 0

    resobj = SqlResult(
        result=result,
        rescode=rescode,
        errormsg=errormsg,
        rowcnt=rowcnt
    )

    if resobj.rescode == 0:
        raise DBException(resobj.errormsg)
    return resobj


def select_list(conn, sql_query, sql_args=None):
    """
    Выполняет запрос к бд, предполагающий результат в виде нескольких строк.
    """
    res = execute(conn, sql_query, sql_args).result
    return res


def select_obj(conn, sql_query, sql_args=None):
    """
    Выполняет запрос к бд, предполагающий результат в виде одной строки.
    """
    res = execute(conn, sql_query, sql_args).result
    return res[0] if len(res) != 0 else None


def insert(conn, sql_query, sql_args=None):
    """
    Выполняет запрос к бд, предполагающий вставку новой строки.
    Возвращает LAST_INSERT_ID() в случае успеха,
    иначе - возбуждает исключение DBException
    """
    res = execute(conn, sql_query, sql_args).result
    # не проверяем размер res, т.к. процедура всегда должна выполнять SELECT:
    # либо чтобы вернуть LAST_INSERT_ID(), либо чтобы вернуть код ошибки
    res = res[0]
    return res['RESCODE']


# TODO подумать над разницей между delete(...) и update(...)
def delete(conn, sql_query, sql_args=None):
    """
    Выполняет запрос к бд, предполагающий вставку новой строки.
    Возвращает кол-во изменённых строк в случае успеха,
    иначе - возбуждает исключение DBException.
    """
    res = execute(conn, sql_query, sql_args).rowcnt
    return res


def update(conn, sql_query, sql_args=None):
    """
    Выполняет запрос к бд, предполагающий вставку новой строки.
    Возвращает кол-во изменённых строк в случае успеха,
    иначе - возбуждает исключение DBException.
    """
    res = execute(conn, sql_query, sql_args).rowcnt
    return res


def get_db():
    db = mysql.connector.connect(**config.DATABASE)
    return db


@contextmanager
def connection():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        yield cursor
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cursor.close()
        db.close()

if __name__ == '__main__':
    with connection() as conn:
        print(select_obj(conn, 'SELECT 1 AS RES'))
        print(select_obj(conn, 'SELECT 2 AS RES'))
        print(connection.__dict__)
