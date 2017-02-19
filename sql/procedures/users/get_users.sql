USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_ALL_USERS $$
CREATE PROCEDURE GET_ALL_USERS()
COMMENT 'Возвращает всех пользователей с указанием их роли'
BEGIN
    SELECT
            U.USER_ID,
            U.LOGIN,
            EMAIL,
            R.NAME as 'ROLE',
            U.PASSWORD,
            U.ENABLE as 'USER_ENABLE'
        FROM
            user as U
            JOIN role as R 
                ON U.ROLE_ID = R.ROLE_ID;
END
$$

DROP PROCEDURE IF EXISTS GET_USER_BY_ID;
CREATE PROCEDURE GET_USER_BY_ID(
    IN vID INT
)
COMMENT 'Возвращает конкретного пользователя по его id с указанием роли'
BEGIN
    SELECT
            U.USER_ID,
            U.LOGIN,
            U.EMAIL,
            R.NAME as 'ROLE',
            U.PASSWORD,
            U.ENABLE as 'USER_ENABLE'
        FROM
            user as U
            JOIN role as R
                ON U.ROLE_ID = R.ROLE_ID
        WHERE
            U.USER_ID = vID;
END
$$

DROP PROCEDURE IF EXISTS GET_USER_BY_LOGIN;
CREATE PROCEDURE GET_USER_BY_LOGIN(
    IN vLOGIN VARCHAR(255)
)
COMMENT 'Возвращает конкретного пользователя по его login с указанием роли'
BEGIN
    SELECT
            U.USER_ID,
            U.LOGIN,
            U.EMAIL,
            R.NAME as 'ROLE',
            U.PASSWORD,
            U.ENABLE as 'USER_ENABLE'
        FROM
            user as U
            JOIN role as R
                ON U.ROLE_ID = R.ROLE_ID
        WHERE
            U.LOGIN = vLOGIN;
END
$$

DELIMITER ;
