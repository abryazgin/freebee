# from flask import
from models import User, Chat
from models.db_worker import DBException
from controllers import ApiController


class UserController(ApiController):

    def __init__(self):
        super().__init__()

