#coding:utf-8
from flask import Blueprint

main = Blueprint("main",__main__)

from . import errors,views