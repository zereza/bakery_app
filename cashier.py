import os
import os.path
from flask import Flask, render_template, request, url_for, Blueprint, flash, redirect
from logging import FileHandler, WARNING
from datetime import datetime
from models import User, Products, Order, db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, IntegerField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
my_cashier = Blueprint("cashier", "cashier", static_folder="static", template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)


@my_cashier.route('/', methods=["POST", "GET"])
@login_required
def cashier_panel():
    return render_template("cashier_panel.html")
