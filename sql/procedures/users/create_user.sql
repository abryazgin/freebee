USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS CREATE_USER $$
CREATE PROCEDURE CREATE_USER (
    IN vLOGIN VARCHAR(255),
    IN vEMAIL VARCHAR(255),
    IN vPASSWORD VARCHAR(255),
    IN vROLE VARCHAR(255)
)
COMMENT 'Добавляет в бд нового пользователя'
PROC : BEGIN
    CALL USER_VERIFY(
        0, vLOGIN, vEMAIL, vROLE,
        @resultcode, @errormsg
    );
    
    IF @resultcode = 0 THEN
        SELECT 0 AS RESCODE, @errormsg as MSG;
        LEAVE PROC;
    END IF;
    
    -- Добавляем пользователя, возвращаем id нового пользователя
    -- в качестве кода завершения процедуры.
    INSERT INTO
        user (LOGIN, EMAIL, PASSWORD, ROLE_ID) VALUES
            (vLOGIN, vEMAIL, vPASSWORD, @roleid);
            
    SELECT LAST_INSERT_ID() AS RESCODE;
END
$$

DELIMITER ;
