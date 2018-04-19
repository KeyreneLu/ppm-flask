#coding:utf-8
from flask_wtf import Form 
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from ..models import User
from wtforms import ValidationError

class LoginForm(Form):
	"""登录表单类"""
	email = StringField("Email",validators=[Required(),Length(1,64),Email()])
	password = PasswordField("Password",validators=[Required()])
	remember_me = BooleanField("记住我")
	submit = SubmitField("登录")

class RegisterForm(Form):
	"""用户注册表单类"""
	email = StringField("Email",validators=[Required(),Length(1,64),Email()])
	username = StringField("Username",validators=[Required(),Length(1,64),Regexp("^[A-Za-z][A-Za-z0-9_.]*$",0,"输入用户不合法")])
	password = PasswordField("password",validators=[Required(),EqualTo("password2",message="两次需一样")])
	password2 = PasswordField("Confirm Password",validators=[Required()])
	submit = SubmitField("注册")

	def validate_email(self,field):
		"""验证邮箱是否存在，validationError为massage提醒内容"""
		if User.query.filter_by(email=field.data).first():
			raise ValidationError("该邮箱已被注册")

	def validate_username(self,field):
		"""验证用户名是否存在"""
		if User.query.filter_by(username=field.data).first():
			raise ValidationError("该用户名")