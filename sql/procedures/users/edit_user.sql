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
    -- Верификация: проверка существования роли
    SELECT
            R.role_id
        INTO
            @roleid
        FROM
            role as R
        WHERE
            R.NAME = vROLE;
    
    IF @roleid IS NULL THEN
        SELECT 0 AS RESCODE, CONCAT('Роль не существует: ', vROLE) AS MSG;
        LEAVE PROC;
    END IF;
    
    -- Верификация: проверка на уникальность логина и email
    SELECT
            U.LOGIN
        INTO
            @existing_login
        FROM
            user as U
        WHERE
            U.LOGIN = vLOGIN;
            
    SELECT
            U.EMAIL
        INTO
            @existing_email
        FROM
            user as U
        WHERE
            U.EMAIL = vEMAIL;
            
    IF @existing_email IS NOT NULL OR @existing_login IS NOT NULL THEN
        SELECT
                0 AS RESCODE,
                CONCAT('Логин и/или email уже заняты: ',
                    @existing_email, ', ', @existing_login)
                    AS MSG;
    LEAVE PROC;
    END IF;
    
    -- Добавляем пользователя, возвращаем код успешного заверешния
    -- процедуры: 1 и id нового пользователя
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
PROC : BEGIN
    -- Верификация: проверка, что пользователь существует:
    SELECT
            LOGIN
        INTO
            @deleted_id
        FROM
            user
        WHERE
            USER_ID = vUSER_ID;
    
    IF @deleted_id IS NULL THEN
        SELECT
            0 AS RESCODE,
            CONCAT('Пользователя с id = ', vUSER_ID, ' не существует')
                AS MSG;
        LEAVE PROC;
    END IF;
    
    DELETE
        FROM
            user
        WHERE
            USER_ID = vUSER_ID;
    
    SELECT 1 AS RESCODE;
END
$$

DELIMITER ;
