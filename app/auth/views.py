#conding:utf-8
from flask import render_template,flash,url_for,request,redirect
from . import auth
from flask_login import login_user,logout_user,login_required,current_user
from .forms import LoginForm,RegisterForm
from ..models import User
from .. import db
from ..email import send_email


@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed and request.blueprint  !="auth" and request.endpoint !="static":
		return redirect(url_for("auth.unconfirmed"))

@auth.route("/unconfirmed")
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for("main.index"))
	return render_template("auth/unconfirmed.html")

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
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email(user.email,"Confirm your Account","auth/email/confirm",user=user,token=token)
		flash("注册成功，请前往邮箱进行验证！")
		return redirect(url_for("main.index"))
	return render_template("auth/register.html",form=form)

@auth.route("/confirm/<token>")
@login_required
def confirm(token):
	"""邮箱验证接口"""
	if current_user.confirmed:
		return redirect(url_for(main.index))
	if current_user.confirm(token):
		flash("邮箱验证成功，正在跳转...")
	else:
		flash("邮箱验证失败或者链接已失效，请重新验证..")
	return redirect(url_for("main.index"))

@auth.route("/confirm")
@login_required
def resend_confirmation():
	"""验证重新发送邮件"""
	token = current_user.generate_confirmation_token();
	send_email(current_user.email,"Confirm Your Account","auth/email/confirm",user=current_user,token=token)
	flash("验证信息已发送，请前往验证")
	return redirect(url_for("main.index"))