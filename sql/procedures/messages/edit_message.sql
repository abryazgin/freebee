USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS CREATE_MESSAGE $$
CREATE PROCEDURE CREATE_MESSAGE (
    IN vUSER_ID INT,
    IN vCHAT_ID INT,
    IN vSEND_TIME DATETIME,
    IN vMESS_TEXT TEXT
)
COMMENT 'Добавляет в бд новое сообщение'
PROC : BEGIN
    CALL MESSAGE_VERIFY(
        0, vUSER_ID, vCHAT_ID,
        vSEND_TIME, vMESS_TEXT,
        @resultcode, @errormsg);
        
    IF @resultcode = 0 THEN
        SELECT 0 AS RESCODE, @errormsg AS MSG;
        LEAVE PROC;
    END IF;
    
    SELECT
            UCH.user_in_chat_id
        INTO
            @uchid
        FROM 
            user_in_chat as UCH
        WHERE
            UCH.USER_ID = vUSER_ID AND
            UCH.CHAT_ID = vCHAT_ID;
    INSERT
        INTO
            message (USER_IN_CHAT_ID, SEND_TIME, MESS_TEXT)
        VALUES
            (@uchid, vSEND_TIME, vMESS_TEXT);
            
    SELECT LAST_INSERT_ID() AS RESCODE;
END
$$

DROP PROCEDURE IF EXISTS DELETE_MESSAGE_BY_ID $$
CREATE PROCEDURE DELETE_MESSAGE_BY_ID (
    IN vMESSAGE_ID INT
)
COMMENT 'Удаялет из бд сообщение с предварительной проверкой на существование'
PROC : BEGIN
    CALL MESSAGE_ID_VERIFY(vMESSAGE_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT
            0 AS RESCODE,
            CONCAT('Сообщения с id = ', vMESSAGE_ID, ' не существует.') as MSG;
        LEAVE PROC;
    END IF;
    
    DELETE
        FROM
            message
        WHERE
            MESSAGE_ID = vMESSAGE_ID;
            
    SELECT 1 AS RESCODE;
END
$$

DROP PROCEDURE IF EXISTS UPDATE_MESSAGE $$
CREATE PROCEDURE UPDATE_MESSAGE (
    IN vMESSAGE_ID INT,
    IN vUSER_ID INT,
    IN vCHAT_ID INT,
    IN vSEND_TIME DATETIME,
    IN vMESS_TEXT TEXT
)
COMMENT 'Изменяет параметры сообщения с id = vMESSAGE_ID'
PROC : BEGIN
    CALL MESSAGE_VERIFY(
        vMESSAGE_ID, vUSER_ID, vCHAT_ID,
        vSEND_TIME, vMESS_TEXT,
        @resultcode, @errormsg);
        
    IF @resultcode = 0 THEN
        SELECT 0 AS RESCODE, @errormsg AS MSG;
        LEAVE PROC;
    END IF;
    
    SELECT
            UCH.user_in_chat_id
        INTO
            @uchid
        FROM 
            user_in_chat as UCH
        WHERE
            UCH.USER_ID = vUSER_ID AND
            UCH.CHAT_ID = vCHAT_ID;
    
    UPDATE
            message as M
        SET
            M.USER_IN_CHAT_ID = @uchid,
            M.SEND_TIME = vSEND_TIME,
            M.MESS_TEXT =vMESS_TEXT 
        WHERE
            M.MESSAGE_ID = vMESSAGE_ID;
            
    SELECT 1 AS RESCODE;
END
$$

DELIMITER ;
