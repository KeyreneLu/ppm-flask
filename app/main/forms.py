#conding:utf-8
from flask_wtf import Form 
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class NameForm(Form):
	"""名字表单类"""
	name = StringField("what is your name?",validators = [Required()])
	submit = SubmitField("submit")


