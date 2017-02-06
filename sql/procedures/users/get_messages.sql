USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_USER_MESSAGES $$
CREATE PROCEDURE GET_USER_MESSAGES(
    IN vUSER_ID INT
)
COMMENT 'Возвращает список всех собщений пользователя'
BEGIN
    SELECT
            M.MESSAGE_ID,
            M.MESS_TEXT,
            M.SEND_TIME,
            M.ENABLE,
            CH.CHAT_ID,
            CH.NAME as 'CHAT_NAME',
            CH.ENABLE
        FROM
            message as M
            JOIN user_in_chat as UCH
                ON M.USER_IN_CHAT_ID = UCH.USER_IN_CHAT_ID
            JOIN chat as CH
                ON CH.CHAT_ID = UCH.CHAT_ID
        WHERE
            UCH.USER_ID = vUSER_ID
        ORDER BY
            M.SEND_TIME DESC;
END
$$

DROP PROCEDURE IF EXISTS GET_USER_LAST_MESSAGES $$
CREATE PROCEDURE GET_USER_LAST_MESSAGES(
    IN vUSER_ID INT,
    IN vMESS_COUNT INT
)
COMMENT 'Возвращает список всех собщений пользователя'
BEGIN
    SELECT
            M.MESSAGE_ID,
            M.MESS_TEXT,
            M.SEND_TIME,
            M.ENABLE,
            CH.CHAT_ID,
            CH.NAME as 'CHAT_NAME',
            CH.ENABLE
        FROM
            message as M
            JOIN user_in_chat as UCH
                ON M.USER_IN_CHAT_ID = UCH.USER_IN_CHAT_ID
            JOIN chat as CH
                ON CH.CHAT_ID = UCH.CHAT_ID
        WHERE
            UCH.USER_ID = vUSER_ID
        ORDER BY
            M.SEND_TIME DESC
        LIMIT
            vMESS_COUNT;
END
$$
