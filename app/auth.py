from flask import request

from app.helpers import get_token_querystring
TOKEN = "pq72KttXvPNZWC7zdLANzUsQYwDd5H2s"


def authenticate(func):
    def inner(*args, **kwargs):
        token = get_token_querystring(request)
        if token == TOKEN:
            return func(kwargs['username'])

        return "Unauthorized", 401
    return inner