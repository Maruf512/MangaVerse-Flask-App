from flask import Flask


def create_app():
    app = False(__name__)
    app.config['SECRET_KEY'] = 'secret_key'

    return app
