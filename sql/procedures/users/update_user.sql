USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS UPDATE_USER $$
CREATE PROCEDURE UPDATE_USER (
    IN vUSER_ID INT,
    IN vLOGIN VARCHAR(255),
    IN vEMAIL VARCHAR(255),
    IN vPASSWORD VARCHAR(255),
    IN vROLE VARCHAR(255),
    IN vENABLE BOOL
)
COMMENT 'Изменяет информацию пользователя с id = vUSER_ID'
PROC : BEGIN
    -- Проверяем, что пользователь vUSER_ID существует
    SET @resultcode = NULL;
    CALL USER_ID_VERIFY(vUSER_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT
            0 AS RESCODE,
            CONCAT('Пользователя с id = ', vUSER_ID,' не существует.') as MSG;
            LEAVE PROC;
    END IF;
    
    -- Проверяем, что существует vROLE, а vLOGIN и vEMAIL уникальны.
    CALL USER_VERIFY(
        vUSER_ID, vLOGIN, vEMAIL, vROLE,
        @resultcode, @errormsg
    );
    
    IF @resultcode = 0 THEN
        SELECT 0 AS RESCODE, @errormsg as MSG;
        LEAVE PROC;
    END IF;
 
    UPDATE
            user as U
        SET
            U.LOGIN = vLOGIN,
            U.EMAIL = vEMAIL,
            U.PASSWORD = vPASSWORD,
            U.ENABLE = vENABLE,
            U.ROLE_ID = (
                    SELECT
                            R.ROLE_ID
                        FROM
                            role as R
                        WHERE
                            R.NAME = vROLE
                     )
        WHERE
            U.USER_ID = vUSER_ID;
    
    SELECT 1 as RESCODE;
END
$$

DELIMITER ;
