from flask import Flask, render_template, request, redirect, url_for, session, current_app
from flask_session import Session
import mysql.connector
from datetime import datetime
import os
import pymysql
from flask_sqlalchemy import SQLAlchemy 
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = 'odfhgdfgjkjbsdfkvnjsdfn'  # Bắt buộc để sử dụng session, nên thay đổi thành chuỗi ngẫu nhiên
# ---- Cấu hình lưu session trên server ----
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://kheuser:123@localhost/flask_sessions_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Cấu hình session
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)  
app.config["SESSION_SQLALCHEMY"] = SQLAlchemy(app)


Session(app)

with app.app_context():
    app.config["SESSION_SQLALCHEMY"].create_all()


#----------------Limit sessions-----------------------
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "20 per minute"]
)
#------------------------------------------------

# Kết nối MySQL
db = mysql.connector.connect(
    host="localhost",
    user="kheuser",
    password="123",
    database="flask_login_demo"
)
cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET', 'POST'])
@limiter.limit("5 per minute")   # giới hạn 5 lần login / phút / IP
def login():

    if 'username' in session:
        return redirect(url_for('welcome'))


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = username  # Lưu vào session
            session['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session.permanent = True  # Đặt session là permanent
            return redirect(url_for('welcome'))

        else:
            return "Sai tên đăng nhập hoặc mật khẩu!"

    return render_template('login.html')


@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('welcome.html', username=session['username'], login_time=session['login_time'])


#@app.route('/logout')
#def logout():
#    #session.pop('username', None)
#    session.clear()
#    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()  # Xóa toàn bộ session của user
    return redirect(url_for('login'))



@app.route('/session-info')
def session_info():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('session_info.html', session_data=session)

if __name__ == '__main__':
    app.run(debug=True)

