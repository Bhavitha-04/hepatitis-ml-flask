from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Ensure full absolute path
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "hepatitis.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Simple test table
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(f"Database created at: {db_path}")
