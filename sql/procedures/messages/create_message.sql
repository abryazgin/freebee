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

DELIMITER ;
