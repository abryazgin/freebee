USE freebee;


INSERT INTO user (LOGIN, PASSWORD, EMAIL, ROLE_ID) VALUES
    ('admin', 'admpass', 'smth1@ex.com', (SELECT ROLE_ID FROM role WHERE NAME = 'admin')), 
    ('john', 'sta1pass', 'smth2@ex.com', (SELECT ROLE_ID FROM role WHERE NAME = 'staffer')), 
    ('mike', 'sta2pass', 'smth3@ex.com', (SELECT ROLE_ID FROM role WHERE NAME = 'staffer')), 
    ('paul', 'cli1pass', 'smth4@ex.com', (SELECT ROLE_ID FROM role WHERE NAME = 'client')), 
    ('ringo', 'cli2pass', 'smth5@ex.com', (SELECT ROLE_ID FROM role WHERE NAME = 'client')), 
    ('george', 'cli3pass', 'smth6@ex.com', (SELECT ROLE_ID FROM role WHERE NAME = 'client'));


INSERT INTO chat (NAME) VALUES
    ('support-1'), ('order-1'), ('order-2');


INSERT INTO user_in_chat (USER_ID, CHAT_ID) VALUES
    ((SELECT USER_ID FROM user WHERE LOGIN = 'admin'),
    (SELECT CHAT_ID FROM chat WHERE NAME = 'support-1')),
    ((SELECT USER_ID FROM user WHERE LOGIN = 'john'),
    (SELECT CHAT_ID FROM chat WHERE NAME = 'support-1')),

    ((SELECT USER_ID FROM user WHERE LOGIN = 'mike'),
    (SELECT CHAT_ID FROM chat WHERE NAME = 'order-1')),
    ((SELECT USER_ID FROM user WHERE LOGIN = 'paul'),
    (SELECT CHAT_ID FROM chat WHERE NAME = 'order-1')),

    ((SELECT USER_ID FROM user WHERE LOGIN = 'john'),
    (SELECT CHAT_ID FROM chat WHERE NAME = 'order-2')),
    ((SELECT USER_ID FROM user WHERE LOGIN = 'ringo'),
    (SELECT CHAT_ID FROM chat WHERE NAME = 'order-2')),
    ((SELECT USER_ID FROM user WHERE LOGIN = 'george'),
    (SELECT CHAT_ID FROM chat WHERE NAME = 'order-2'));


INSERT INTO message (USER_IN_CHAT_ID, SEND_TIME, MESS_TEXT) VALUES
    ((SELECT USER_IN_CHAT_ID FROM user_in_chat
    WHERE
    user_in_chat.USER_ID = (SELECT USER_ID FROM user WHERE user.LOGIN = 'john')
    AND
    user_in_chat.CHAT_ID = (SELECT CHAT_ID FROM chat WHERE chat.NAME = 'support-1')),
    '2017-01-05 16:15:22',
    'Добрый день.'),

    ((SELECT USER_IN_CHAT_ID FROM user_in_chat
    WHERE
    USER_ID = (SELECT USER_ID FROM user WHERE user.LOGIN = 'admin')
    AND
    CHAT_ID = (SELECT CHAT_ID FROM chat WHERE chat.NAME = 'support-1')),
    '2017-01-05 16:16:22',
    'Добрый день.'),


    ((SELECT USER_IN_CHAT_ID FROM user_in_chat
    WHERE
    USER_ID = (SELECT USER_ID FROM user WHERE user.LOGIN = 'admin')
    AND
    CHAT_ID = (SELECT CHAT_ID FROM chat WHERE chat.NAME = 'support-1')),
    '2017-01-05 16:17:10',
    'Чем могу помочь?'),
     
    ((SELECT USER_IN_CHAT_ID FROM user_in_chat
    WHERE
    USER_ID = (SELECT USER_ID FROM user WHERE user.LOGIN = 'mike')
    AND
    CHAT_ID = (SELECT CHAT_ID FROM chat WHERE chat.NAME = 'order-1')),
    '2017-01-05 14:12:25',
    'Привет!');
