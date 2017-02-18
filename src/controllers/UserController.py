# from flask import
from models import User, Chat
from models.db_worker import DBException
from controllers import BaseController


class UserController(BaseController):

    def __init__(self):
        super().__init__()

