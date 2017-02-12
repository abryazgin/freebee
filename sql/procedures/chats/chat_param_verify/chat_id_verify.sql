USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS CHAT_ID_VERIFY;
CREATE PROCEDURE CHAT_ID_VERIFY(
    IN vCHAT_ID INT,
    OUT vRESCODE INT
)
COMMENT 'Проверяет существование чата с данным vCHAT_ID.
        Возвращает vRESCODE:
                0 - чат с vCHAT_ID не существует,
                1 - чат с vCHAT_ID существует;'
PROC : BEGIN
    SET @chatid = NULL;
    SELECT
            CH.CHAT_ID
        INTO
            @chatid
        FROM
            chat as CH
        WHERE 
            CH.CHAT_ID = vCHAT_ID;
    
    IF @chatid IS NULL THEN
        SET vRESCODE = 0;
        LEAVE PROC;
    END IF;
    
    -- Чат существует:
    -- SELECT 1 INTO vRESCODE;
    SET vRESCODE = 1;
END
$$

DELIMITER ;
 
