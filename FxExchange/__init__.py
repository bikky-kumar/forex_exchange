from pickle import FALSE
from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()

DB_NAME =  "database.sqlite3"

def create_app():
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = 'fx_exchange'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = FALSE
    db.init_app(app)
  


    #import views
    from .views import views

    #register with flask app
    app.register_blueprint(views, url_prefix='/')

    from .models import Transaction
    create_database(app)


    return app 

def create_database(app):
    if not path.exists('FxExchange/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database')