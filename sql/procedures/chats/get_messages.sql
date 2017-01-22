USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_CHAT_MESSAGES $$
CREATE PROCEDURE GET_CHAT_MESSAGES(
    IN vCHAT_ID INT
)
COMMENT 'Возвращает полный список сообщей в данном чате'
BEGIN
    SELECT
            M.MESSAGE_ID,
            M.SEND_TIME,
            M.MESS_TEXT,
            U.USER_ID
        FROM
            message as M
            JOIN user_in_chat as UCH
                ON UCH.USER_IN_CHAT_ID = M.USER_IN_CHAT_ID
            JOIN user as U
                ON U.USER_ID = UCH.USER_ID
        WHERE
            UCH.CHAT_ID = vCHAT_ID
        ORDER BY
            M.SEND_TIME DESC;
END
$$

DROP PROCEDURE IF EXISTS GET_LAST_CHAT_MESSAGES $$
CREATE PROCEDURE GET_LAST_CHAT_MESSAGES(
    IN vCHAT_ID INT,
    IN vMESS_COUNT INT
)
COMMENT 'Возвращает полный список сообщей в данном чате'
BEGIN
    SELECT
            M.MESSAGE_ID,
            M.SEND_TIME,
            M.MESS_TEXT,
            U.USER_ID
        FROM
            message as M
            JOIN user_in_chat as UCH
                ON UCH.USER_IN_CHAT_ID = M.USER_IN_CHAT_ID
            JOIN user as U
                ON U.USER_ID = UCH.USER_ID
        WHERE
            UCH.CHAT_ID = vCHAT_ID
        ORDER BY
            M.SEND_TIME DESC
        LIMIT
            vMESS_COUNT;
END
$$

DELIMITER ;
