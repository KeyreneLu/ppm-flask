#coding:utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET = "PPM19940321"
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	FLASKY_MAIL_SUBJECT_PREFIX = "BlogProj"
	FLASKY_MAIL_SENDER = "BlogProj Admin"
	FLASKY_ADMIN = "KeyreneLu"

	@staticmethod
	def init__app(app):
		pass

class DevelopmentConfig(config):
	"""开发环境配置"""
	debug = True
	MAIL_SERVER = "smtp.googlemail.com"
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
	SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
	"sqlite:///"+os.path.join(basedir,"data.dev.sqlite")

class TestingConfig(config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
	"sqlite:///" + os.path.join(basedir,"data.test.sqlite")

class ProductionConfig(config):
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
	"sqlite:///" + os.path.join(basedir,"data.sqlite")

config = {
	"development":DevelopmentConfig
	"testing":TestingConfig
	"production":ProductionConfig

	"default":DevelopmentConfig
}