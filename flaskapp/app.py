import os
from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as mysql
import argparse

app = Flask(__name__)

def establish_connection():
    """
    gain connection
    """
    cnx = mysql.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        auth_plugin='mysql_native_password'
    )
    return cnx

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        con=establish_connection()
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        if cur.fetchone():
            cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email))
        else:
            cur.execute("CREATE TABLE users (name varchar(20), email varchar(40));")
            cur.execute("INSERT INTO users(name, email) VALUES(%s, %s)",(name, email))
        con.commit()
        con.close()
        return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    con=establish_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    userDetails=cur.fetchall()
    if len(userDetails) > 0:
        return render_template('users.html',userDetails=userDetails)

@app.route('/all')
def all():
    con=establish_connection()
    cur = con.cursor()
    #cur.execute("SELECT * FROM users")
    cur.execute("SELECT name FROM * WHERE type='table';")
    tables = cur.fetchall()
    tables=cur.fetchall()
    #if len(userDetails) > 0:
    return render_template('users.html',tables=tables)

@app.route('/allx')
def allx():
    con = establish_connection()
    cur = con.cursor()

    # Get all table names from MySQL
    cur.execute("SHOW TABLES;")
    tables = [table[0] for table in cur.fetchall()]

    db_dump = {}

    for table_name in tables:
        cur.execute(f"SELECT * FROM `{table_name}`")  # Use backticks for safety
        rows = cur.fetchall()

        # Get column names
        col_names = [desc[0] for desc in cur.description]

        # Store table data as list of dicts
        db_dump[table_name] = [dict(zip(col_names, row)) for row in rows]

    con.close()

    return jsonify(db_dump)
    #return render_template(db_dump)


@app.route('/version')
def version():
    try:
        with open("/etc/hostname", "r") as f:
            container_id = f.read().strip()
        return(f"Container ID: {container_id}")
    except Exception as e:
        return(f"Unexpected error when detecting container ID: {e}")

#@jsonrpc.method('app.index')
#def index(a):
#    return 'hello {a}'.format(a=a)

@app.route('/wheewhoo')
def whee():
    con=establish_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    userDetails=cur.fetchall()
    if len(userDetails) > 0:
        return render_template('users.html',userDetails=userDetails)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='lorem ipsum')

    parser.add_argument('--dry-run', action='store_true', help='Test that the app can be run, quit afterwards')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port to run the Flask app on (default is 5000)')

    args = parser.parse_args()

    if args.dry_run:
        print(f"Dry run - do nothing.")
    else:
        app.run(host='0.0.0.0', debug=True, port=args.port)

