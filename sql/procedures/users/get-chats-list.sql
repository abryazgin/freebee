USE freebee;

DELIMITER //

DROP PROCEDURE IF EXISTS GET_CHAT_LIST_BY_LOGIN;
CREATE PROCEDURE GET_CHAT_LIST_BY_LOGIN(IN LOG VARCHAR(255))
COMMENT 'Возвращает список чатов данного пользователя'
BEGIN
    SELECT
            CH.CHAT_ID,
            CH.NAME
        FROM
            chat as CH
        JOIN user_in_chat as UCH ON UCH.CHAT_ID = CH.CHAT_ID
        JOIN user as U ON U.USER_ID = UCH.USER_ID
        WHERE
            U.LOGIN = LOG;
END
//
