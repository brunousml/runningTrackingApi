from flask import Flask, request
from app.views import api

app = Flask(__name__)
app.register_blueprint(api)
