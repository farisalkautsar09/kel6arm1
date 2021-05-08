import random
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import json
import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'risss'
app.config['MYSQL_DB'] = 'production'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        status = request.form['status']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                if request.form['status'] == user["status"]:
                    return render_template("home.html")
                else: 
                    return "Akun anda belum terverifikasi, silahkan hubungi pihak kami!"
            else:
                return "Error password and email not match"
        else:
            return "Error user not found"
    else:
        return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        posisi = request.form['select']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
        (name, email, hash_password, posisi))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('login'))

@app.route('/busi')
def busi():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM busi")
    rv = cur.fetchall()
    cur.close()
    return render_template('busi.html', busis=rv)


@app.route('/insert-busi', methods=["POST"])
def insertBusi():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.datetime.strptime(startDate, "%m/%d/%Y %I:%M %p")
    end = datetime.datetime.strptime(endDate, "%m/%d/%Y %I:%M %p")
    deltaTgl = end - start

    cur = mysql.connection.cursor()

    Delete_all_rows = """truncate table busi """
    cur.execute(Delete_all_rows)
    mysql.connection.commit()

    for x in range(deltaTgl.days + 1):
        target = random.randint(126, 137)
        aktual = random.randint(127, 142)
        status = ''

        if aktual < target:
            status = 'under performance'
        elif aktual > target :
            status ='performance'
        else :
            status = 'on target'

        date = start + datetime.timedelta(days=x)
        tanggal = date.strftime("%d/%m/%Y")
        
        cur.execute("INSERT INTO busi (tanggal, target, aktual, status) VALUES (%s, %s, %s, %s)", (tanggal, target, aktual, status))
        mysql.connection.commit()

    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return "success"
    else:
        return redirect(url_for('busi'))

@app.route('/aki')
def aki():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM aki")
    rv = cur.fetchall()
    cur.close()
    return render_template('aki.html', akis=rv)

@app.route('/insert-aki', methods=["POST"])
def insertAki():
    startDate = request.form['startDate']
    endDate = request.form['endDate']
    start = datetime.datetime.strptime(startDate, "%m/%d/%Y %I:%M %p")
    end = datetime.datetime.strptime(endDate, "%m/%d/%Y %I:%M %p")
    deltaTgl = end - start

    cur = mysql.connection.cursor()

    Delete_all_rows = """truncate table aki """
    cur.execute(Delete_all_rows)
    mysql.connection.commit()

    for x in range(deltaTgl.days + 1):
        target = random.randint(50, 60)
        aktual = random.randint(50, 70)
        status = ''

        if aktual < target:
            status = 'under performance'
        elif aktual > target :
            status ='performance'
        else :
            status = 'on target'

        date = start + datetime.timedelta(days=x)
        tanggal = date.strftime("%d/%m/%Y")

        cur.execute("INSERT INTO aki (tanggal, target, aktual, status) VALUES (%s, %s, %s, %s)", (tanggal, target, aktual, status))
        mysql.connection.commit()

    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return "success"
    else:
        return redirect(url_for('aki'))

@app.route('/update-user', methods=["POST"])
def updateUser():
    id_data = request.form['id']
    email = request.form['email']
    name = request.form['nama']
    status = request.form['status']
    role = request.form['role']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET email=%s, name=%s, status=%s, role=%s WHERE id=%s", (email, name, status, role, id_data,))
    mysql.connection.commit()
    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return "success"
    else:
        return redirect(url_for('admin'))

@app.route('/admin', methods=["GET"])
def admin():
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM users")
    fv = curl.fetchall()
    curl.close()
    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return json.dumps(fv)
    else:
        return render_template("admin.html", users=fv)

@app.route('/apply', methods=["POST"])
def apply():
    id_users = request.form['id']
    status = request.form['apply']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET status=%s WHERE id=%s", (status, id_users))
    mysql.connection.commit()
    return redirect(url_for('admin'))

@app.route('/about-us')
def AboutUs():
    isMobile = request.args.get('mobile')
    if isMobile == "true":
        return "json succes" #json.dumps(users)
    else:
        return render_template("about-us.html")

if __name__ == '__main__':
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(host='0.0.0.0',debug=True)
