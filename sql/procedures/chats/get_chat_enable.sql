USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_CHAT_ENABLE;
CREATE PROCEDURE GET_CHAT_ENABLE(
    IN vCHAT_ID INT,
    OUT vENABLE INT
)
COMMENT 'Возвращает свойство ENABLE чата'
PROC : BEGIN
	CALL CHAT_ID_VERIFY(vCHAT_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT
            0 as RESCODE,
            CONCAT('Чата с id = ', vCHAT_ID, ' не существует.');
            LEAVE PROC;
    END IF; 
	
	SET vENABLE = NULL;
	SELECT
			CH.ENABLE
		INTO
			vENABLE
		FROM
			chat as CH
		WHERE
			CH.CHAT_ID = vCHAT_ID;
END
$$

DELIMITER ;
