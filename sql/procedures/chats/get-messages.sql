USE freebee;

DELIMITER //

DROP PROCEDURE IF EXISTS GET_MESSAGES;
CREATE PROCEDURE GET_MESSAGES(IN CHAT_ID INT)
COMMENT 'Возвращает полный список сообщей в данном чате'
BEGIN
    SELECT
            M.MESSAGE_ID,
            M.SEND_TIME as 'send time',
            M.MESS_TEXT as 'text',
            U.LOGIN as 'sender login',
            C.NAME as 'chat name'
        FROM
            message as M
        JOIN user_in_chat as UCH ON UCH.USER_IN_CHAT_ID = M.USER_IN_CHAT_ID
        JOIN user as U ON U.USER_ID = UCH.USER_ID
        JOIN chat as C ON C.CHAT_ID = CHAT_ID
        WHERE
            UCH.CHAT_ID = CHAT_ID;
END
//

DROP PROCEDURE IF EXISTS GET_LAST_MESSAGES;
CREATE PROCEDURE GET_LAST_MESSAGES(IN CHAT_ID INT, IN MESS_COUNT INT)
COMMENT 'Возвращает полный список сообщей в данном чате'
BEGIN
    SELECT
            M.MESSAGE_ID,
            M.SEND_TIME as 'send time',
            M.MESS_TEXT as 'text',
            U.LOGIN as 'sender login'
        FROM
            message as M
        JOIN user_in_chat as UCH ON UCH.USER_IN_CHAT_ID = M.USER_IN_CHAT_ID
        JOIN user as U ON U.USER_ID = UCH.USER_ID
        WHERE
            UCH.CHAT_ID = CHAT_ID
        ORDER BY
            M.SEND_TIME
        LIMIT
            MESS_COUNT;
END
