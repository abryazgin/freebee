USE freebee;

DELIMITER $$

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

DELIMITER ;
