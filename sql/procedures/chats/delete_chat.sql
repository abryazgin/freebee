USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS DELETE_CHAT_BY_ID $$
CREATE PROCEDURE DELETE_CHAT_BY_ID (
    IN vCHAT_ID INT
)
COMMENT 'Удаляет чат из бд с предварительной проверкой на сущетсвование.
        Также будет удалена информация о "вхождениях" пользователей в
        данный чат и все сообщения, отправленные в данный чат.'
PROC : BEGIN
    CALL CHAT_ID_VERIFY(vCHAT_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT 0 as RESCODE,
        CONCAT('Чата с id = ', vCHAT_ID, ' не существует.');
        LEAVE PROC;
    END IF;
    
    -- Стираем все сообщения в удаляемом чате.
    DELETE message
        FROM
            message
            JOIN user_in_chat ON
                message.USER_IN_CHAT_ID = user_in_chat.USER_IN_CHAT_ID
            WHERE
                user_in_chat.CHAT_ID = vCHAT_ID;
            
    -- Стираем информацию о пользователях чата.
    DELETE
        FROM
            user_in_chat
        WHERE
            user_in_chat.CHAT_ID = vCHAT_ID;
    
    -- Удаляем сам чат.
    DELETE
        FROM
            chat
        WHERE
            CHAT_ID = vCHAT_ID;
            
    SELECT 1 as RESCODE;
END
$$

DELIMITER ;

