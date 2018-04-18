#coding:utf-8
from datetime import datetime
from flask import render_template,session,redirect

from . import main
from .forms import NameForm
from .. import db
from ..models import Role,User

@main.route("/",methods=["GET","POST"])
def index():
	form = NameForm()
	if form.validate_on_submit():
		old_name = session.get("name")
		if old_name is not None and old_name != form.name.data:
			flash("you looks like change your name")
			return redirect(url_for(".index"))
	return render_template("index.html",form=form,name=session.get("name"),
		known = session.get("known",False),current_time=datetime.utcnow())