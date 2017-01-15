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
BEGIN
    SELECT
            R.role_id
        INTO
            @roleid
        FROM
            role as R
        WHERE
            R.NAME = vROLE;
    
    INSERT INTO
        user (LOGIN, EMAIL, PASSWORD, ROLE_ID) VALUES
            (vLOGIN, vEMAIL, vPASSWORD, @roleid);
            
    SELECT
            LAST_INSERT_ID() as NEW_ID;
END
$$

DROP PROCEDURE IF EXISTS DELETE_USER_BY_ID $$
CREATE PROCEDURE DELETE_USER_BY_ID (
    IN vUSER_ID INT
)
BEGIN
    DELETE
        FROM
            user
        WHERE
            USER_ID = vUSER_ID;
END
$$

DELIMITER ;
