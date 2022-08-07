from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'yellowpages'

mysql = MySQL(app)

@app.route('/')
@app.route('/company', methods=['GET', 'POST'])
def users():
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute('SELECT * FROM company')
    companies = conn.fetchall()
    return render_template('company.html', companies=companies)

@app.route('/addrecord', methods=['GET', 'POST'])
def addrecord():
    msg=''
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        website = request.form['website']
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute('SELECT * FROM company WHERE phone = % s', (phone,))
        account = conn.fetchone()
        if account:
            msg = 'Company already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address'
        elif not name or not phone or not email or not address:
            msg = 'Please fill all details'
        else:
            conn.execute('INSERT INTO company VALUES (NULL, % s, % s, % s, % s, % s)'
                         '', (name, email, phone, address, website,))
            mysql.connection.commit()
            msg = 'You have successfully added !'
            return render_template('addrecord.html', msg=msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('addrecord.html', msg=msg)

@app.route('/rupdate', methods=['GET', 'POST'])
def rupdate():
    msg='Failed to update'
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        website = request.form['website']
        print()
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute("UPDATE company SET name='{}', address='{}', phone={}, website='{}', email='{}' "
                     "where id={}".format(name,address, phone, website, email,id))
        mysql.connection.commit()
        msg = 'Record successfully updated !'
        return redirect('/')
    return render_template('updaterecord.html', msg=msg)

@app.route('/updaterecord/<id>', methods=['GET', 'POST'])
def updaterecord(id):
    msg=''
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute("SELECT * FROM company where id={}".format(id))
    record = conn.fetchone()
    return render_template('updaterecord.html', company=record)

@app.route('/deleterecord/<id>', methods=['GET', 'POST'])
def deleterecord(id):
    msg=''
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute("DELETE FROM company where id={}".format(id))
    mysql.connection.commit()
    msg = 'Record successfully deleted !'
    return redirect('/')

