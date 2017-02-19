USE freebee;

DELIMITER $$


DROP PROCEDURE IF EXISTS ADD_USER_IN_CHAT $$
CREATE PROCEDURE ADD_USER_IN_CHAT (
    IN vUSER_ID INT,
    IN vCHAT_ID INT
)
COMMENT 'Добавляет пользователя vUSER_ID в чат vCHAT_ID'
PROC : BEGIN
    CALL CHECK_USER_IN_CHAT(
        vUSER_ID,
        vCHAT_ID,
        @resultcode,
        @errormsg);
    
    IF @resultcode = 1 THEN
        SELECT 0 as RESCODE,
        CONCAT('Пользователь id = ', vUSER_ID,
               ' уже добавлен в чат id = ', vCHAT_ID)
                as MSG;
        LEAVE PROC;
    END IF;
    
    IF @resultcode = -1 THEN
        SELECT 0 as RESCODE, @errormsg as MSG;
        LEAVE PROC;
    END IF;
    
    INSERT INTO
        user_in_chat (CHAT_ID, USER_ID) VALUES
            (vCHAT_ID, vUSER_ID);
            
    SELECT LAST_INSERT_ID() as RESCODE;
END
$$

DELIMITER ;
