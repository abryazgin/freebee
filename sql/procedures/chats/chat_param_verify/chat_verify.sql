USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS CHECK_USER_IN_CHAT $$
CREATE PROCEDURE CHECK_USER_IN_CHAT (
    IN vUSER_ID INT,
    IN vCHAT_ID INT,
    OUT vRESCODE INT,
    OUT vMSG VARCHAR(255)
)
COMMENT 'Проверяет, входит ли данный пользователь в данный чат
        Возвращает
            - vRESCODE:
               -1 - чат/пользователь не существует;
                0 - пользователь не входит в чат;
                1 - пользователь входит в чат.
            - vMSG: сообщение об ошибке.'
PROC2 : BEGIN
    -- проверка на существование чата
    CALL CHAT_ID_VERIFY(vCHAT_ID, @resultcode);
    IF @resultcode = 0 THEN
            SET vRESCODE = -1;
            SET vMSG = CONCAT('Чата с id = ', vCHAT_ID, ' не существует.');
            LEAVE PROC2;
    END IF;
    
    -- проверка на существование пользователя
    CALL USER_ID_VERIFY(vUSER_ID, @resultcode);
        IF @resultcode = 0 THEN
            SET vRESCODE = -1;
            SET vMSG = CONCAT('Пользователя с id = ', vUSER_ID, ' не существует.');
            LEAVE PROC2;
    END IF;

    -- проверка на вхождение пользователя в чат
    SET @uchid = NULL;
    SELECT
            UCH.USER_IN_CHAT_ID
        INTO
            @uchid
        FROM 
            user_in_chat as UCH
        WHERE
            UCH.USER_ID = vUSER_ID AND
            UCH.CHAT_ID = vCHAT_ID;
    
    IF @uchid IS NULL THEN
        SET vRESCODE = 0;
        LEAVE PROC2;
    END IF;
    
    SET vRESCODE = 1;
END
$$

DELIMITER ;
