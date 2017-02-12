USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS GET_USER_IN_CHAT_ENABLE;
CREATE PROCEDURE GET_USER_IN_CHAT_ENABLE(
    IN vCHAT_ID INT,
    IN vUSER_ID INT,
    OUT vENABLE INT
)
COMMENT 'Возвращает ENABLE пользователя vUSER_ID в vCHAT_ID.
		 Возвращает 0, если чат или юзер имеют ENABLE равное 0.'
PROC : BEGIN
	CALL CHECK_USER_IN_CHAT(
        vUSER_ID,
        vCHAT_ID,
        @resultcode,
        @errormsg);
        
    IF @resultcode = -1 THEN
		SELECT 
			0 as RESCODE,
			CONCAT('Чата/пользователя с id = ', vCHAT_ID, '/', vUSER_ID, ' не существует.');
        LEAVE PROC;
    END IF;
    
    IF @resultcode = 0 THEN
		SELECT 
			0 as RESCODE,
			CONCAT('Пользователь id = ', vUSER_ID,
			' не входит в чат id = ', vCHAT_ID);
        LEAVE PROC;
    END IF;
    
    CALL GET_USER_ENABLE(vUSER_ID, @user_enable);
    CALL GET_CHAT_ENABLE(vCHAT_ID, @chat_enable);
    
    IF @user_enable = 0 OR @chat_enable = 0 THEN
		SET vENABLE = 0;
		LEAVE PROC;
    END If;
    
    SELECT
			UCH.ENABLE
		INTO
			vENABLE
		FROM
			user_in_chat as UCH
		WHERE
			UCH.CHAT_ID = vCHAT_ID AND
			UCH.USER_ID = vUSER_ID;
END
$$

DELIMITER ;
