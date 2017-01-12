USE freebee;

DELIMITER //

DROP PROCEDURE IF EXISTS GET_ALL_USERS;
CREATE PROCEDURE GET_ALL_USERS()
COMMENT 'Возвращает всех пользователей с указанием их роли'
BEGIN
    SELECT
            U.USER_ID,
            U.LOGIN,
            EMAIL,
            R.NAME as 'role',
            U.PASSWORD
        FROM
            user as U
        JOIN role as R ON U.ROLE_ID = R.ROLE_ID;
END
//


DROP PROCEDURE IF EXISTS GET_USER_BY_LOGIN;
CREATE PROCEDURE GET_USER_BY_LOGIN(IN LOG VARCHAR(255))
COMMENT 'Возвращает конкретного пользователя с указанием роли'
BEGIN
    SELECT
            U.USER_ID,
            U.LOGIN,
            U.EMAIL,
            R.NAME as 'role',
            U.PASSWORD
        FROM
            user as U
        JOIN role as R ON U.ROLE_ID = R.ROLE_ID
            WHERE
            U.LOGIN = LOG;
END
//
