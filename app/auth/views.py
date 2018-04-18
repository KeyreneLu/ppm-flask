#conding:utf-8
from flask import render_template,flash,url_for,request,redirect
from . import auth
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm
from ..models import User

@auth.route("/login",methods=["GET","POST"])
def login():
	"""用户登录方法"""
	form = LoginForm()
	if form.validate_on_submit:
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get("next") or url_for("main.index"))
		flash("用户名或密码错误")
	return render_template("auth/login.html",form=form)

@auth.route("/logout")
@login_required
def logout():
	"""用户登出接口"""
	logout_user()
	flash("用户已登出")
	return redirect(url_for("main.index"))
