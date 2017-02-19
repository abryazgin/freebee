USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_CHATS $$
CREATE PROCEDURE GET_CHATS()
COMMENT 'Возвращает всех список чатов'
BEGIN
    SELECT
            CH.CHAT_ID,
            CH.NAME,
            CH.ENABLE
        FROM
            chat as CH;
END

$$
