USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS UPDATE_MESSAGE $$
CREATE PROCEDURE UPDATE_MESSAGE (
    IN vMESSAGE_ID INT,
    IN vUSER_ID INT,
    IN vCHAT_ID INT,
    IN vSEND_TIME DATETIME,
    IN vMESS_TEXT TEXT,
    IN vENABLE BOOL
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
            M.MESS_TEXT = vMESS_TEXT ,
            M.ENABLE = vENABLE
        WHERE
            M.MESSAGE_ID = vMESSAGE_ID;
            
    SELECT 1 AS RESCODE;
END
$$

DELIMITER ;
