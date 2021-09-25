import os
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True


SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/casting'