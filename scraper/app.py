import requests
import time
import os
from flask import Flask, render_template, request, redirect
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

def inject_data(name):
        email = "thisem@nono.com"
        con=establish_connection()
        cur = con.cursor()
        cur.execute("SHOW TABLES")
        tables = [table[0] for table in cur.fetchall()]

        if "scraper" in tables:
            cur.execute("INSERT INTO scraper(name, email) VALUES(%s, %s)",(name, email))
        else:
            cur.execute("CREATE TABLE scraper (name varchar(20), email varchar(40));")
            cur.execute("INSERT INTO scraper(name, email) VALUES(%s, %s)",(name, email))
        con.commit()
        con.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='lorem ipsum')

    parser.add_argument('--dry-run', action='store_true', help='Test that the app can be run, quit afterwards')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port to run the Flask app on (default is 5000)')

    args = parser.parse_args()

    print(f"Scraper is beginning...")

    if args.dry_run:
        print(f"Dry run - do nothing.")
    else:
        i = 0

        # Loop over, just pushing some dummy values into the database
        while True:
            print('i')

            inject_data(i)
            i += 1
            time.sleep(50)
