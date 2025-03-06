import requests
import time
import os
import mysql.connector as mysql
import argparse

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the base model
Base = declarative_base()

# Define the Scraper table as a SQLAlchemy model - cleaner
class Scraper(Base):
    __tablename__ = "scraper_data"

    name = Column(String(20), primary_key=True)
    value = Column(Integer, nullable=False)

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

def inject_data(value):
    name = f"Test data {value}"
    session = manager.session()

    # Check if the entry already exists
    existing_entry = session.query(Scraper).filter_by(name=name).first()
    if not existing_entry:
        session.add(Scraper(name=name, value=value))
        session.commit()

    session.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='lorem ipsum')

    parser.add_argument('--dry-run', action='store_true', help='Test that the app can be run, quit afterwards')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port to run the Flask app on (default is 5000)')

    args = parser.parse_args()

    print(f"Scraper is beginning...")

    if args.dry_run:
        print(f"Dry run - do nothing.")
    else:
        manager.connect()
        i = 100

        # Loop over, just pushing some dummy values into the database
        while True:
            print(f'iteration {i}')

            inject_data(i)
            i += 1
            time.sleep(50)
