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

        if "dataa" in tables:
            cur.execute("INSERT INTO dataa(name, email) VALUES(%s, %s)",(name, email))
        else:
            cur.execute("CREATE TABLE dataa (name varchar(20), email varchar(40));")
            cur.execute("INSERT INTO dataa(name, email) VALUES(%s, %s)",(name, email))
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
        #app.run(host='0.0.0.0', debug=True, port=args.port)

        # CoinMetrics API endpoint
        url = "https://api.coinmetrics.io/v4/timeseries/asset-metrics"

        # Query parameters
        params = {
            "assets": "btc",
            "metrics": "HashRate",
            "frequency": "1d",
            "start_time": "2024-01-01",
            "end_time": "2024-02-01",
            "api_key": "YOUR_API_KEY"  # Replace with your CoinMetrics API key if required
        }

        # Make the request
        #response = requests.get(url, params=params)

        ## Check for successful response
        #if response.status_code == 200:
        #    data = response.json()
        #    for entry in data["data"]:
        #        print(f"Date: {entry['time']}, Hash Rate: {entry['HashRate']}")
        #else:
        #    print(f"Error: {response.status_code}, {response.text}")

        i = 0

        while True:
            print('i')

            inject_data(i)
            i += 1
            time.sleep(50)
