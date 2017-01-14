CREATE USER 'freebee'@'%' IDENTIFIED BY '221uml?Po';
GRANT ALL on freebee.* to 'freebee'@'%';
SELECT user, host FROM mysql.user;