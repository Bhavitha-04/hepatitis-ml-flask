from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# ==========================
# Create Flask app
# ==========================
app = Flask(__name__)

# ==========================
# Configure SQLite database
# ==========================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hepatitis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ==========================
# Initialize database
# ==========================
db = SQLAlchemy(app)

# ==========================
# User table
# ==========================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # store hashed password
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

# ==========================
# Health profile table
# ==========================
class HealthProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    alcohol_use = db.Column(db.Boolean, default=False)
    past_liver_issue = db.Column(db.Boolean, default=False)
    pregnancy_history = db.Column(db.Boolean, default=False)
    medications = db.Column(db.String(200))

# ==========================
# Questionnaire responses table
# ==========================
class QuestionnaireResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    fatigue = db.Column(db.Boolean, default=False)
    appetite_loss = db.Column(db.Boolean, default=False)
    nausea = db.Column(db.Boolean, default=False)
    fever = db.Column(db.Boolean, default=False)
    joint_pain = db.Column(db.Boolean, default=False)
    abdominal_pain = db.Column(db.Boolean, default=False)
    bloating = db.Column(db.Boolean, default=False)
    weight_loss = db.Column(db.Boolean, default=False)
    post_meal_discomfort = db.Column(db.Boolean, default=False)
    jaundice = db.Column(db.Boolean, default=False)
    dark_urine = db.Column(db.Boolean, default=False)
    pale_stool = db.Column(db.Boolean, default=False)
    itching = db.Column(db.Boolean, default=False)
    duration_gt_1w = db.Column(db.Boolean, default=False)
    worsening = db.Column(db.Boolean, default=False)
    recurring = db.Column(db.Boolean, default=False)
    risk_level = db.Column(db.String(20))

# ==========================
# Create all tables when run directly
# ==========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully!")
