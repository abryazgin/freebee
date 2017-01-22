USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS MESSAGE_ID_VERIFY $$
CREATE PROCEDURE MESSAGE_ID_VERIFY(
    IN vMESSAGE_ID INT,
    OUT vRESCODE INT
)
COMMENT 'Проверяет существование сообщения с данным vMESSAGE_ID
        Возвращает: vRESCODE:
            0 - сообщение не существует;
            1 - сообщение существует'
PROC : BEGIN
    SET @messid = NULL;
    SELECT
            M.MESSAGE_ID
        INTO
            @messid
        FROM
            message as M
        WHERE
            M.MESSAGE_ID = vMESSAGE_ID;
    
    IF @messid IS NULL THEN
        SET vRESCODE = 0;
        LEAVE PROC;
    END IF;
    
    SET vRESCODE = 1;
END
$$

DROP PROCEDURE IF EXISTS MESSAGE_VERIFY $$
CREATE PROCEDURE MESSAGE_VERIFY(
    IN vMESSAGE_ID INT,
    IN vUSER_ID INT,
    IN vCHAT_ID INT,
    IN vSEND_TIME DATETIME,
    IN vMESS_TEXT TEXT,
    OUT vRESCODE INT,
    OUT vMSG VARCHAR(255)
)
COMMENT 'Проверяет существование пользователя vUSER_ID, чата vCHAT_ID
        и входит ли пользователь vUSER_ID в чат vCHAT_ID.
            
        Возвращает:
            - vRESCODE:
                0 - в случае ошибки,
                1 - в случае успешной верификации;
            - vMSG:
                сообщение об ошибке.'
PROC : BEGIN
    -- TODO проверить:
    IF  
        vMESSAGE_ID IS NULL OR
        vUSER_ID IS NULL OR
        vCHAT_ID IS NULL OR
        vSEND_TIME IS NULL OR
        vMESS_TEXT IS NULL
    THEN
        SET vRESCODE = 0;
        SET vMSG = CONCAT(
                    'Один из параметров NULL:',
                    ' vMESSAGE_ID = ', vMESSAGE_ID,
                    ', vUSER_ID = ', vUSER_ID,
                    ', vCHAT_ID = ', vCHAT_ID,
                    ', vSEND_TIME = ', vSEND_TIME,
                    ', vMESS_TEXT = ', vMESS_TEXT);
        LEAVE PROC;
    END IF;
    
    CALL CHECK_USER_IN_CHAT(
        vUSER_ID,
        vCHAT_ID,
        @resultcode,
        @errormsg);
        
    IF @resultcode = 0 THEN
        SET vRESCODE = 0;
        SET vMSG = CONCAT('Пользователь id = ', vUSER_ID,
               ' не входит в чат id = ', vCHAT_ID);
        LEAVE PROC;
    END IF;
    
    IF @resultcode = -1 THEN
        SET vRESCODE = 0;
        SET vMSG = @errormsg;
        LEAVE PROC;
    END IF;
    
    SET vRESCODE = 1;
END
$$

DELIMITER ;
