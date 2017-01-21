USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_CHAT_LIST_BY_USER_ID $$
CREATE PROCEDURE GET_CHAT_LIST_BY_USER_ID(
    IN vID INT
)
COMMENT 'Возвращает список чатов данного пользователя'
BEGIN
    SELECT
            CH.CHAT_ID,
            CH.NAME
        FROM
            chat as CH
            JOIN user_in_chat as UCH
                ON UCH.CHAT_ID = CH.CHAT_ID
            JOIN user as U
                ON U.USER_ID = UCH.USER_ID
        WHERE
            U.USER_ID = vID;
END
$$

DELIMITER ;
