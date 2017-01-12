USE freebee;


SELECT 
        LOGIN,
        EMAIL,
        role.NAME as 'role',
        PASSWORD 
    FROM 
        user 
        JOIN role 
            ON user.ROLE_ID = role.ROLE_ID;


SELECT
		CH.NAME as 'chat name',
		U.LOGIN as 'user login'
	FROM
	user_in_chat as UCH
		JOIN user as U ON UCH.USER_ID = U.USER_ID
		JOIN chat as CH ON UCH.CHAT_ID = CH.CHAT_ID;


SELECT 
        user.LOGIN as 'user login', 
        SEND_TIME, 
        chat.NAME as 'chat name', 
        MESS_TEXT
    FROM 
        message 
        JOIN user_in_chat 
            ON user_in_chat.USER_IN_CHAT_ID = message.USER_IN_CHAT_ID
        JOIN user 
            ON user.USER_ID = user_in_chat.USER_ID
        JOIN chat 
            ON chat.CHAT_ID = user_in_chat.CHAT_ID
    WHERE 
        TRUE;
