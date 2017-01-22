USE freebee;

DELIMITER $$

DROP PROCEDURE IF EXISTS CREATE_CHAT $$
CREATE PROCEDURE CREATE_CHAT (
    IN vNAME VARCHAR(225)
)
COMMENT 'Добавляет в бд новый чат'
BEGIN
    -- Проверок не требуется, к названию чата нет требования на уникальность
    INSERT INTO
        chat (name) VALUES (vNAME);
    SELECT LAST_INSERT_ID() as RESCODE;
END
$$

DROP PROCEDURE IF EXISTS DELETE_CHAT_BY_ID $$
CREATE PROCEDURE DELETE_CHAT_BY_ID (
    IN vCHAT_ID INT
)
COMMENT 'Удаляет чат из бд с предварительной проверкой на сущетсвование.
        Также будет удалена информация о "вхождениях" пользователей в
        данный чат и все сообщения, отправленные в данный чат.'
PROC : BEGIN
    CALL CHAT_ID_VERIFY(vCHAT_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT 0 as RESCODE,
        CONCAT('Чата с id = ', vCHAT_ID, ' не существует.');
        LEAVE PROC;
    END IF;
    
    -- Стираем все сообщения в удаляемом чате.
    DELETE message
        FROM
            message
            JOIN user_in_chat ON
                message.USER_IN_CHAT_ID = user_in_chat.USER_IN_CHAT_ID
            WHERE
                user_in_chat.CHAT_ID = vCHAT_ID;
            
    -- Стираем информацию о пользователях чата.
    DELETE
        FROM
            user_in_chat
        WHERE
            user_in_chat.CHAT_ID = vCHAT_ID;
    
    -- Удаляем сам чат.
    DELETE
        FROM
            chat
        WHERE
            CHAT_ID = vCHAT_ID;
            
    SELECT 1 as RESCODE;
END
$$

DROP PROCEDURE IF EXISTS UPDATE_CHAT $$
CREATE PROCEDURE UPDATE_CHAT (
    IN vCHAT_ID INT,
    IN vNAME VARCHAR(255)
)
COMMENT 'Изменяет информацию о чате с id = vCHAT_ID'
PROC : BEGIN
    CALL CHAT_ID_VERIFY(vCHAT_ID, @resultcode);
    
    IF @resultcode = 0 THEN
        SELECT
            0 as RESCODE,
            CONCAT('Чата с id = ', vCHAT_ID, ' не существует.');
            LEAVE PROC;
    END IF;
    
    UPDATE chat as CH
        SET
            CH.NAME = vNAME
        WHERE
            CH.CHAT_ID = vCHAT_ID;
            
    SELECT 1 as RESCODE;
END
$$

DROP PROCEDURE IF EXISTS ADD_USER_IN_CHAT $$
CREATE PROCEDURE ADD_USER_IN_CHAT (
    IN vUSER_ID INT,
    IN vCHAT_ID INT
)
COMMENT 'Добавляет пользователя vUSER_ID в чат vCHAT_ID'
PROC : BEGIN
    CALL CHECK_USER_IN_CHAT(
        vUSER_ID,
        vCHAT_ID,
        @resultcode,
        @errormsg);
    
    IF @resultcode = 1 THEN
        SELECT 0 as RESCODE,
        CONCAT('Пользователь id = ', vUSER_ID,
               ' уже добавлен в чат id = ', vCHAT_ID)
                as MSG;
        LEAVE PROC;
    END IF;
    
    IF @resultcode = -1 THEN
        SELECT 0 as RESCODE, @errormsg as MSG;
        LEAVE PROC;
    END IF;
    
    INSERT INTO
        user_in_chat (CHAT_ID, USER_ID) VALUES
            (vCHAT_ID, vUSER_ID);
            
    SELECT LAST_INSERT_ID() as RESCODE;
END
$$

DROP PROCEDURE IF EXISTS REMOVE_USER_FROM_CHAT $$
CREATE PROCEDURE REMOVE_USER_FROM_CHAT (
    IN vUSER_ID INT,
    IN vCHAT_ID INT
)
COMMENT 'Удаляет пользователя vUSER_ID из чата vCHAT_ID'
PROC : BEGIN
    CALL CHECK_USER_IN_CHAT(
        vUSER_ID,
        vCHAT_ID,
        @resultcode,
        @errormsg);
    
    IF @resultcode = 0 THEN
        SELECT 0 as RESCODE,
        CONCAT('Пользователь id = ', vUSER_ID,
               ' не входит в чат id = ', vCHAT_ID)
        as MSG;
        LEAVE PROC;
    END IF;
    
    IF @resultcode = -1 THEN
        SELECT 0 as RESCODE,
        @errormsg as MSG;
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
    
    -- Стираем "вхождение" пользователя в чат
    DELETE
        FROM
            user_in_chat
        WHERE
            user_in_chat.USER_ID = vUSER_ID AND
            user_in_chat.CHAT_ID = vCHAT_ID;
            
    SELECT 1 as RESCODE;
END
$$

DELIMITER ;

