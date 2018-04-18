#coding:utf-8
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_find(e):
	"""404路径错误界面"""
	return render_template("404.html"),404

@main.app_errorhandler(500)
def inernal_server_error(e):
	"""500系统错误界面"""
	return render_template("500.html"),500