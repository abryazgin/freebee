USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS USER_ID_VERIFY;
CREATE PROCEDURE USER_ID_VERIFY(
    IN vUSER_ID INT,
    OUT vRESCODE INT
)
COMMENT 'Проверяет существование пользователя с данным vUSER_ID.
        Возвращает:
            - vRESCODE:
                0 - пользователя с vUSER_ID не существует,
                1 - пользователь с vUSER_ID существует;'
PROC : BEGIN
    SET @userid = NULL;
    SELECT
            U.USER_ID
        INTO
            @userid
        FROM
            user as U
        WHERE 
            U.USER_ID = vUSER_ID;
    
    IF @userid IS NULL THEN
        SET vRESCODE = 0;
        LEAVE PROC;
    END IF;
    
    -- Пользователь существует:
    -- SELECT 1 INTO vRESCODE;
    SET vRESCODE = 1;
END
$$

DELIMITER ;
