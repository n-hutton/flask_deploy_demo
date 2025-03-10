import os
from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector as mysql
import argparse
from sqlalchemy import create_engine, Column, String, Integer, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the base model
Base = declarative_base()

# Define the Scraper table as a SQLAlchemy model - cleaner
class User(Base):
    __tablename__ = "user_data"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(120), unique=True, nullable=False)

class DatabaseManager():
    session = None

    def connect(self):
        # SQLAlchemy engine for cleaner execution
        DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
        engine = create_engine(DATABASE_URL, echo=True)

        # Create the table if it doesn't exist
        Base.metadata.create_all(engine)

        # Create a session factory
        SessionLocal = sessionmaker(bind=engine)
        self.session = SessionLocal

manager = DatabaseManager()
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']

        session = manager.session()

        # Check if the entry already exists
        existing_entry = session.query(User).filter_by(name=name).first()
        if not existing_entry:
            session.add(User(name=name, email=email))
            session.commit()
        return redirect('/users')
    return render_template('index.html')

@app.route('/users')
def users():
    session = manager.session()
    userDetails = session.query(User).all()

    return render_template('users.html', userDetails=userDetails)

@app.route('/all')
def all():
    """
    Show everything in the database as JSON.
    """
    db_dump = {}

    session = manager.session()
    try:
        inspector = inspect(session.bind)  # Get metadata about the database

        for table_name in inspector.get_table_names():
            # Execute a query to fetch all records
            table_data = session.execute(text(f"SELECT * FROM `{table_name}`")).mappings().all()

            # Convert rows to list of dictionaries
            db_dump[table_name] = [dict(row) for row in table_data]

    finally:
        session.close()  # Ensure session is closed

    return jsonify(db_dump)


"""
Display which pod we are in/version
"""
@app.route('/version')
def version():
    try:
        with open("/etc/hostname", "r") as f:
            container_id = f.read().strip()
        return(f"Container ID: {container_id}")
    except Exception as e:
        return(f"Unexpected error when detecting container ID: {e}")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='lorem ipsum')

    parser.add_argument('--dry-run', action='store_true', help='Test that the app can be run, quit afterwards')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port to run the Flask app on (default is 5000)')

    args = parser.parse_args()

    if args.dry_run:
        print(f"Dry run - do nothing.")
    else:
        manager.connect()
        app.run(host='0.0.0.0', debug=True, port=args.port)

