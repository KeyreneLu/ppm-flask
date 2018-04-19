#conding:utf-8
from flask import render_template,flash,url_for,request,redirect
from . import auth
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm,RegisterForm
from ..models import User
from .. import db

@auth.route("/login",methods=["GET","POST"])
def login():
	"""用户登录方法"""
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get("next") or url_for("main.index"))
		if form.email.data is not None and form.password.data is not None:
			flash("用户名或密码错误")
	return render_template("auth/login.html",form=form)

@auth.route("/logout")
@login_required
def logout():
	"""用户登出接口"""
	logout_user()
	flash("用户已登出")
	return redirect(url_for("main.index"))

@auth.route("/register",methods=["GET","POST"])
def register():
	"""用户注册接口"""
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(email=form.email.data,username=form.username.data,
			password=form.password.data)
		db.session.add(user)
		flash("注册成功，可前往登录")
		return redirect(url_for("auth.login"))
	return render_template("auth/register.html",form=form)