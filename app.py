from flask import Flask, render_template, request, session, flash
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
import os

app = Flask(__name__)
Bootstrap(app)

#Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #This is we can use .name .age and not [0],[1]
mysql = MySQL(app)

app.config['SECRET_KEY'] = os.urandom(24)


@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        try: #This is for the flash message try is right excpt deal with the fail message
            form = request.form
            name = form['name']
            age = form['age']
            cur = mysql.connection.cursor()
            # name = generate_password_hash(name) #This takes the password(name) and hashes it. 
            cur.execute("INSERT INTO employee(name, age) VALUES(%s, %s)", (name, age))
            mysql.connection.commit()
            flash('Successfully', 'success')
        except:
            flash('Failed to insert data','danger')
    return render_template('index.html')


@app.route('/employees')
def employees():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM employee")
    if result_value > 0:
        employees = cur.fetchall()
        #check_password_hash(employees[1]['name'], '123456') # chck to see if password are same will boolen
        session['username'] = employees[0]['name']
        return render_template('employees.html', employees=employees)

if __name__ == "__main__":
    app.run(debug=True, port=5000)