USE freebee;

DELIMITER $$

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
