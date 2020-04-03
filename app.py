from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

#Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #This is we can use .name .age and not [0],[1]
mysql = MySQL(app)


@app.route('/', methods=['GET', "POST"])
def index():
    if request.method == 'POST':
        form = request.form
        name = form['name']
        age = form['age']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee(name, age) VALUES(%s, %s)", (name, age))
        mysql.connection.commit()
    return render_template('index.html')


@app.route('/employees')
def employees():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM employee")
    if result_value > 0:
        employees = cur.fetchall()
        return render_template('employees.html', employees=employees)

if __name__ == "__main__":
    app.run(debug=True, port=5000)