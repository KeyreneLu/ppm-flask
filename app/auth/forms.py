#coding:utf-8
from flask_wtf import Form 
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Length,Email

class LoginForm(Form):
	"""登录表单类"""
	email = StringField("Email",validators=[Required(),Length(1,64),Email()])
	password = StringField("Password",validators=[Required()])
	remember_me = BooleanField("记住我")
	submit = SubmitField("登录")