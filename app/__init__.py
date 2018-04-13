#coding:utf-8
from flask import Flask,render_template
from flask-bootstrap import Bootstrap
from flask-mail import Mail
from flask-moment import Moment
from flask-sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
	"""app生产工厂类"""
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init__app(app)

	bootstrap.init__app(app)
	mail.init__app(app)
	moment.init__app(app)
	db.init__app(app)

	#附加路由和自定义的错误界面
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app

