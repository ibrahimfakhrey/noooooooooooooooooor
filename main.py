# make api call with this key to get the weather of banha

import json
import os

from flask_babel import Babel
from sqlalchemy.orm import joinedload
from flask import Flask, render_template, redirect, url_for, flash, abort, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart





import requests
app=Flask(__name__)
babel = Babel(app)

appid="868c5469fc5add3122d3e7e8313c8f3e"
# web = "https://api.openweathermap.org/data/3.0/onecall?lat=33.44&lon=-94.04&appid={868c5469fc5add3122d3e7e8313c8f3e}"
# x= input("plese ebter the name of the city")
# END_POINT="https://api.openweathermap.org/data/2.5/weather"
# params={
#     "q":"banha",
#     "appid":appid
#     ,"units":"metric"
# }
#
# response=requests.get(END_POINT,params)
# data=response.json()
# temp=data["main"]["temp"]

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Check if user is in paid_user table
    user = User.query.get(int(user_id))
    if user:
        return user
    # If not, check if user is in free_user table

    # If user is not in either table, return None


app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():



    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))









    db.create_all()


class MyModelView(ModelView):
    def is_accessible(self):
        return True


admin = Admin(app)
admin.add_view(MyModelView(User, db.session))



@app.route("/")
def start():
    return render_template("landing page.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        phone=request.form.get("phone")
        password=request.form.get("password")
        user=User.query.filter_by(phone=phone).first()
        if user and password==user.password:
            login_user(user)
            return redirect("/dash")
        else:
            return "not registered"


    return render_template("login.html")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        phone=request.form.get("phone")
        password=request.form.get("password")
        name=request.form.get("name")

        new_user=User(phone=phone,password=password,name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/dash")
def dash():
    
    if current_user.is_authenticated :
         return f"welcom to your dash "
    else:
        return redirect("/login")
@app.route("/logout")
def logout():
    logout_user()
    return "logout"
if __name__=="__main__":
    app.run(debug=True)