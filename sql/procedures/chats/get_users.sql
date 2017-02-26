USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_CHAT_USERS $$
CREATE PROCEDURE GET_CHAT_USERS(
    IN vCHAT_ID INT
)
COMMENT 'Возвращает список пользователей данного чата'
BEGIN
    SELECT
            U.USER_ID,
            U.LOGIN,
            U.EMAIL,
            U.PASSWORD,
            R.NAME as 'ROLE',
            U.ENABLE as 'USER_ENABLE'
        FROM user as U
            JOIN user_in_chat as UCH
                ON UCH.USER_ID = U.USER_ID
            JOIN role as R
                ON U.ROLE_ID = R.ROLE_ID
            WHERE
                UCH.CHAT_ID = vCHAT_ID;
END
