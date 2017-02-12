USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS REMOVE_USER_FROM_CHAT $$
CREATE PROCEDURE REMOVE_USER_FROM_CHAT (
    IN vUSER_ID INT,
    IN vCHAT_ID INT
)
COMMENT 'Удаляет пользователя vUSER_ID из чата vCHAT_ID'
PROC : BEGIN
    CALL CHECK_USER_IN_CHAT(
        vUSER_ID,
        vCHAT_ID,
        @resultcode,
        @errormsg);
    
    IF @resultcode = 0 THEN
        SELECT 0 as RESCODE,
        CONCAT('Пользователь id = ', vUSER_ID,
               ' не входит в чат id = ', vCHAT_ID)
        as MSG;
        LEAVE PROC;
    END IF;
    
    IF @resultcode = -1 THEN
        SELECT 0 as RESCODE,
        @errormsg as MSG;
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
    
    -- Стираем "вхождение" пользователя в чат
    DELETE
        FROM
            user_in_chat
        WHERE
            user_in_chat.USER_ID = vUSER_ID AND
            user_in_chat.CHAT_ID = vCHAT_ID;
            
    SELECT 1 as RESCODE;
END
$$

DELIMITER ;
 
