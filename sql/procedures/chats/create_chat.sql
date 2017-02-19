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

DELIMITER ;
