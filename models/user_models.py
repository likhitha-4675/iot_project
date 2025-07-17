from flask import render_template, request, redirect, session
from datetime import datetime
import random
import speedtest

mysql=None
def init_mysql(mysql_obj):
    global mysql
    mysql=mysql_obj

def user_register_route(request, session):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        otp = str(random.randint(100000, 999999)) 
        otp_time = datetime.now()               
        print("Generated OTP:", otp)
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, email, otp, otp_generated_time, is_verified) VALUES (%s, %s, %s, %s, %s)", (username, email, otp, otp_time, False))
        mysql.connection.commit()
        session['email'] = email
        return redirect('/enter_otp')
    return render_template('user_register.html')

def enter_otp_route(request,session):
    if request.method == 'POST':
        entered_otp = ''.join(request.form.getlist('otp'))
        email=session.get('email')
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT otp FROM users WHERE email = %s", [email])
        result = cursor.fetchone()
        if result and entered_otp == str(result[0]):
            cursor.execute("UPDATE users SET is_verified = %s, otp_used_time = %s WHERE email = %s", (True, datetime.now(), email))
            mysql.connection.commit()
            return redirect('/user_dashboard')
        else:
            return "Invalid OTP"
    return render_template('enter_otp.html')

def user_dashboard_route(session):
    email = session.get('email')
    if not email:
        return "Session expired. Please register again."
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, email, internet_speed, usage_data FROM users WHERE email = %s", [email])
    user = cursor.fetchone()
    if user:
        speed = get_real_time_speed(email)
        return render_template('user_dashboard.html',speed=speed)
    return "User not found"
def get_real_time_speed(email):
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000
        real_time_speed = round(download_speed, 2)
        print(f"Internet Speed for {email}: {real_time_speed} Mbps")
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET internet_speed = %s WHERE email = %s", (real_time_speed, email))
        mysql.connection.commit()
        return real_time_speed
        print("Speedtest config error:", e)
    except speedtest.ConfigRetrievalError:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET internet_speed = %s WHERE email = %s", (0, email))
        mysql.connection.commit()
        return 0
def update_usage_data(email, data_used):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET usage_data = %s WHERE email = %s", (data_used, email))
        mysql.connection.commit()
        print(f"Updated usage for {email}: {data_used}")
    except Exception as e:
        print("Error updating usage_data:", e)

def user_dashboard_route(session):
    email = session.get('email')
    if not email:
        return "Session expired. Please register again."
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username, email, internet_speed, usage_data FROM users WHERE email = %s", [email])
    user = cursor.fetchone()
    if user:
        speed = get_real_time_speed(email)
        usage = "520MB"
        update_usage_data(email, usage)
        return render_template('user_dashboard.html', speed=speed, usage=usage)
    return "User not found"



def logout_route(session):
    session.clear()
    return redirect('/user_register')

