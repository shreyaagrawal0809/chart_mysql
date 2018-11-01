from flask import render_template ,send_file, redirect,url_for, request, session, flash
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_googlecharts import GoogleCharts, BarChart
from flask import Flask, flash
from flask_mysqldb import MySQL
import MySQLdb
from flask_appbuilder.charts.views import DirectByChartView
from decimal import Decimal
from matplotlib import pyplot as plt
from io import StringIO, BytesIO
from StringIO import StringIO
import base64
import io
import os
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField,TextField, TextAreaField
from flask_wtf.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_wtf import Form, validators
from logging import DEBUG
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
import pygal

import models
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.logger.setLevel(DEBUG)
app.config['SECRET_KEY'] = 'i\xf0L\x92\xf3\ux95#\x8f\\\x06ZP\xea\x1f1\x04\xb2\x16\xff\xf9\x90\xaf\x18\x99'
#mysql = MySQL(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login_page"
login_manager.init_app(app)


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    return redirect(url_for('hello'))

def connection():
    # Edited out actual values
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="shreya",
                           db = "Assam")
    c = conn.cursor()

    return c, conn
c, con = connection()   

class SignupForm(Form):
  firstname = TextField("First name",validators = [DataRequired()])
  email = TextField("Email",  validators = [DataRequired(), Length(1, 120), Email()])
  password = PasswordField('Password', validators = [DataRequired()])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     

@app.route('/')
@app.route('/index')
def hello():
  flash('Hello there')
  return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
   
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else: 
            username = form.firstname.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            x = c.execute("SELECT * FROM users WHERE username = '{}'".format(thwart(username)))
            if x:
                flash('The username already exists please select new!')
            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",(username,password,email,'/introduction-to-python-programming'))
                con.commit()
                flash('Congratulations you are registered')
                return redirect('login')
                session['logged_in'] = False
                session['username'] = username           
    return render_template('signup.html', form=form)


@app.route('/login', methods = ['GET','POST'])
def login_page():
    error = ''
    if request.method == 'POST':
        data = c.execute("SELECT * FROM users WHERE username = '{}'".format(request.form['username']))
        data = c.fetchone()[2]
        if sha256_crypt.verify(request.form['password'],data):
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('logged in ')
            return redirect(url_for('hello'))  
        error = 'invalide credentials'
    return render_template('login.html', error = error)


Grant = []
values = []
   
#print(Actuals)
c.execute("Select Voted_Changed, Actuals2016_17 from assam_data")
data_ = c.fetchall()

con.commit()

x = []
y = []
A = []
B = []



@app.route('/image/')
def image_chart():
    for i in data_:
        A.append(i[0])
        B.append(i[1])
    plt.xticks(rotation=45)
    sunalt = plt.bar(A,B)
    img = StringIO()
    
    plt.savefig(img, format = 'png')
    img.seek(0)
   
    b2 = base64.b64encode(img.read())
    sunalt2 = b2.decode('utf-8')
    return render_template('image.html', mimetype = 'png', sunalt = sunalt2.decode('utf8'))
@app.route('/fig/')
def fig():
    for i in data_:
        x.append(i[0])
        y.append(i[1])

    plt.plot(x,y)
    img = StringIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype = 'image/png')


if __name__ == '__main__':
    app.run(debug=True)

