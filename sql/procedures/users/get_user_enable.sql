USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_USER_ENABLE;
CREATE PROCEDURE GET_USER_ENABLE(
    IN vUSER_ID INT,
    OUT vENABLE INT
)
COMMENT 'Возвращает свойство ENABLE пользователя'
PROC : BEGIN
	CALL USER_ID_VERIFY(vUSER_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT
            0 as RESCODE,
            CONCAT('Пользователя с id = ', vUSER_ID, ' не существует.');
            LEAVE PROC;
    END IF; 
	
	SET vENABLE = NULL;
	SELECT
			U.ENABLE
		INTO
			vENABLE
		FROM
			user as U
		WHERE
			U.USER_ID = vUSER_ID;
END
$$

DELIMITER ;
 
