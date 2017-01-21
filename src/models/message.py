class Message:
    def __init__(self, id, time, text, sender, chat):
        self.id = id
        self.sender = sender
        self.time = time
        self.text = text
        self.chat = chat

    def __str__(self):
        return ('id = {0}, sender.login = {1}, chat.name = {2}, ' +
                'time = {3}, text = {4}').format(
                self.id, self.sender.login, self.chat.name,
                self.time, self.text)
