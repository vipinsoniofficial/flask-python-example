from flask_sqlalchemy import SQLAlchemy
from server import app, logging

logging.info("In config.py: database Configuration")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)