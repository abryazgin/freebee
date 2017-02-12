USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS UPDATE_CHAT $$
CREATE PROCEDURE UPDATE_CHAT (
    IN vCHAT_ID INT,
    IN vNAME VARCHAR(255),
    IN vENABLE BOOL
)
COMMENT 'Изменяет информацию о чате с id = vCHAT_ID'
PROC : BEGIN
    CALL CHAT_ID_VERIFY(vCHAT_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT
            0 as RESCODE,
            CONCAT('Чата с id = ', vCHAT_ID, ' не существует.');
            LEAVE PROC;
    END IF;
    
    UPDATE chat as CH
        SET
            CH.NAME = vNAME,
            CH.ENABLE = vENABLE
        WHERE
            CH.CHAT_ID = vCHAT_ID;
            
    SELECT 1 as RESCODE;
END
$$

DELIMITER ;
