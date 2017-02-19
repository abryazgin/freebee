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

DELIMITER ;
