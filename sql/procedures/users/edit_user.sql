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

DROP PROCEDURE IF EXISTS DELETE_USER_BY_ID $$
CREATE PROCEDURE DELETE_USER_BY_ID (
    IN vUSER_ID INT
)
COMMENT 'Удаляет пользователя из бд с предварительной проверкой на существование
        Также будут удалены все "вхождения пользователя в чаты и все отправленные
        им сообщения."'
PROC : BEGIN
    SET @resultcode = NULL;
    CALL USER_ID_VERIFY(vUSER_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT
            0 AS RESCODE,
            CONCAT('Пользоватеся с id = ', vUSER_ID,' не существует.') as MSG;
            LEAVE PROC;
    END IF;
    
    -- Стираем все сообщения удаляемого пользователя
    DELETE message
        FROM
            message
            JOIN user_in_chat ON
                message.USER_IN_CHAT_ID = user_in_chat.USER_IN_CHAT_ID
            WHERE
                user_in_chat.USER_ID = vUSER_ID;
    
    -- Стираем информацию о чатах удаляемого пользователя
    DELETE
        FROM
            user_in_chat
        WHERE
            user_in_chat.USER_ID = vUSER_ID;
    
    -- Удаляем самого пользователя
    DELETE
        FROM
            user
        WHERE
            USER_ID = vUSER_ID;
    
    SELECT 1 AS RESCODE;
END
$$

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
