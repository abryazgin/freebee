USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS DELETE_USER_BY_ID $$
CREATE PROCEDURE DELETE_USER_BY_ID (
    IN vUSER_ID INT
)
COMMENT 'Удаляет пользователя из бд с предварительной проверкой на существование
        Также будут удалены все "вхождения пользователя в чаты и все отправленные
        им сообщения."'
PROC : BEGIN
    SET @resultcode = NULL;
    CALL USER_ID_VERIFY(vUSER_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT
            0 AS RESCODE,
            CONCAT('Пользоватеся с id = ', vUSER_ID,' не существует.') as MSG;
            LEAVE PROC;
    END IF;
    
    -- Стираем все сообщения удаляемого пользователя
    DELETE message
        FROM
            message
            JOIN user_in_chat ON
                message.USER_IN_CHAT_ID = user_in_chat.USER_IN_CHAT_ID
            WHERE
                user_in_chat.USER_ID = vUSER_ID;
    
    -- Стираем информацию о чатах удаляемого пользователя
    DELETE
        FROM
            user_in_chat
        WHERE
            user_in_chat.USER_ID = vUSER_ID;
    
    -- Удаляем самого пользователя
    DELETE
        FROM
            user
        WHERE
            USER_ID = vUSER_ID;
    
    SELECT 1 AS RESCODE;
END
$$

DELIMITER ;
