import os

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the file name of the SQLite file
sqlite_file_name = "../database.sqlite"

# Get the base directory of the file
base_dir = os.path.dirname(os.path.realpath(__file__))

# Create the SQLAlchemy database URL
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Create the SQLAlchemy engine
engine = create_engine(database_url, echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)

# Declare the base
Base = declarative_base()
