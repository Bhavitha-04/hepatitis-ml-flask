import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Print current working directory
print("Current working directory:", os.getcwd())

# Create Flask app
app = Flask(__name__)

# Absolute path to DB
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "hepatitis.db")
print("Database will be created at:", db_path)

# Configure SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Test table
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

# Create tables
with app.app_context():
    db.create_all()
    print("Tables created successfully!")
