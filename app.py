from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
import random
import speedtest
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config.from_pyfile('config.py')
mysql = MySQL(app)


@app.route('/')
def home():
    return redirect('/user_register')


@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']

        otp = str(random.randint(100000, 999999)) 
        otp_time = datetime.now()               
        print("Generated OTP:", otp)


        cursor = mysql.connection.cursor()
        cursor.execute("""INSERT INTO users (username, email, otp, otp_generated_time, is_verified) 
        VALUES (%s, %s, %s, %s, %s)
        """, (username, email, otp, otp_time, False))
        mysql.connection.commit()

       
        session['email'] = email


        return redirect('/enter_otp')

    return render_template('user_register.html')


@app.route('/enter_otp', methods=['GET', 'POST'])
def enter_otp():
    if request.method == 'POST':
        entered_otp = ''.join(request.form.getlist('otp'))
        email=session.get('email')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT otp FROM users WHERE email = %s", [email])
        result = cursor.fetchone()
        if result and entered_otp == str(result[0]):
            cursor.execute("""
                UPDATE users SET is_verified = %s, otp_used_time = %s
                WHERE email = %s
            """, (True, datetime.now(), email))
            mysql.connection.commit()

            return redirect('/user_dashboard')
        else:
            return "Invalid OTP"
    return render_template('enter_otp.html')
 

@app.route('/user_dashboard')
def user_dashboard():
    email = session.get('email')
    if not email:
        return "Session expired or not logged in. Please register again."

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT id, username, email, internet_speed, usage_data FROM users WHERE email = %s
    """, [email])    
    user = cursor.fetchone()

    if user:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  
        real_time_speed = round(download_speed, 2)

        cursor.execute("""
            UPDATE users SET internet_speed = %s WHERE email = %s
        """, (real_time_speed,email))
        mysql.connection.commit()

        return render_template('user_dashboard.html',
                               user_id=user[0],
                               name=user[1],
                               email=user[2],
                               speed=real_time_speed, 
                               usage=user[4])
    else:
        return "User not found in database"


@app.route('/logout')
def logout():
    session.clear()  
    return redirect('/user_register')


if __name__ == '__main__':
    app.run(debug=True)
