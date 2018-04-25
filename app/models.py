#conding:utf-8
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Role(db.Model):
	"""角色模型"""
	__tablename__ = "roles"
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64),unique=True)
	users = db.relationship("User",backref="role")

	def __repr__(self):
		return "<Role %r>"%self.name

class User(UserMixin,db.Model):
	"""用户模型"""
	__tablename__ = "users"
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(64),unique=True,index=True)
	username = db.Column(db.String(64),index=True)
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean,default=False)
	role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))

	def __repr__(self):
		return "<User %r>"%self.username

	@property
	def password(self):
		"""读取密码异常"""
		raise AttributeError("Password is not readable attribute")

	@password.setter
	def password(self,password):
		"""获取密码的hash值"""
		self.password_hash = generate_password_hash(password)

	def verify_password(self,password):
		"""验证密码正确性"""
		return check_password_hash(self.password_hash,password)

	def generate_confirmation_token(self,expiration=3600):
		"""用户邮箱验证"""
		s = Serializer(current_app.config["SECRET_KEY"],expiration)
		return s.dumps({"confirm":self.id})

	def confirm(self,token):
		
		s = Serializer(current_app.config["SECRET_KEY"])
		try:
			data = s.loads(token)
		except :
			return False
		if data.get("confirm") != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

@login_manager.user_loader
def load_user(user_id):
	"""加载用户的回调函数，如果能找到用户，这个函数必需返回用户对象，否则返回None"""
	return User.query.get(int(user_id))
