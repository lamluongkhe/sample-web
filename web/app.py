from flask import Flask, render_template, request, redirect, url_for, session, current_app
from flask_session import Session
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'odfhgdfgjkjbsdfkvnjsdfn'  # Bắt buộc để sử dụng session, nên thay đổi thành chuỗi ngẫu nhiên
# ---- Cấu hình lưu session trên server ----
app.config['SESSION_TYPE'] = 'filesystem'  # lưu trên file
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session_data')
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # thời gian sống
Session(app)

# Kết nối MySQL
db = mysql.connector.connect(
    host="mysql",
    user="kheuser",
    password="123",
    database="flask_login_demo"
)
cursor = db.cursor(dictionary=True)

@app.route('/', methods=['GET', 'POST'])
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
    session_id = request.cookies.get(current_app.config['SESSION_COOKIE_NAME'])

    if session_id:
        # Tạo đường dẫn đến file session
        session_file = os.path.join(current_app.config['SESSION_FILE_DIR'], session_id)
        try:
            os.remove(session_file)  # Xóa file session
        except FileNotFoundError:
            pass

    session.clear()  # Xóa session trong Flask
    return redirect(url_for('login'))



@app.route('/session-info')
def session_info():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('session_info.html', session_data=session)

if __name__ == '__main__':
    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
