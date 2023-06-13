from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FileField, IntegerField, DateTimeField
from wtforms.validators import DataRequired

app = Flask(__name__)


class Product_form(FlaskForm):
    catagory = StringField(label='Catagory', validators=[DataRequired()])
    product_name = StringField(label='Product Name', validators=[DataRequired()])
    product_name_th = StringField(label='Thai Name', validators=[DataRequired()])
    price = IntegerField(label='Price', validators=[DataRequired()])
    alias = StringField(label='Alias', validators=[DataRequired()])
    amount = IntegerField(label='Amount', validators=[DataRequired()])
    user = IntegerField(label='User', validators=[DataRequired()])
    date = DateTimeField(label='Time', validators=[DataRequired()])
    promo = BooleanField(label='Promotion', validators=[DataRequired()])
    new = BooleanField(label='New Product', validators=[DataRequired()])