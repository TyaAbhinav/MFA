from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from flask import jsonify
import random

# Initializing Flask application, database, and password hashing
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'mfadb', 'users.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Database Models

# Model for Security Questions
class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200), nullable=False)

# Model for User Details
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    familyname = db.Column(db.String(80), nullable=False)
    answers = db.relationship('UserAnswer', backref='user', lazy=True)

# Model for storing User's answers to Security Questions
class UserAnswer(db.Model):
    answer_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    answer_hash = db.Column(db.String(200), nullable=False)

# Create the database tables if they do not exist
with app.app_context():
    db.create_all()

# Default route to redirect to login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Login Route


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

        # If user doesn't exist, show an error
        if not user:
            return render_template('login.html', error="Username not found.")

        # Fetch user's answers
        user_answers = user.answers
        if len(user_answers) < 3:
            return "Insufficient security questions. Please contact support."

        # Randomly select 3 security questions for the user
        random_user_answers = random.sample(user_answers, 3)
        random_questions = [{'text': Question.query.get(ua.question_id).question_text, 'id': ua.question_id} for ua in random_user_answers]
        
        # If the request expects JSON (i.e., from our testing script), then return a JSON response
        if 'application/json' in request.headers.get('Accept'):
            return jsonify(random_questions=random_questions)

        return render_template('kba.html', random_questions=random_questions, username=username, user=user)

    return render_template('login.html')


# Route to verify user's answers to security questions
@app.route('/kba', methods=['POST'])
def kba():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)

    # Ensure user exists
    if not user:
        return "User not found."
        
    # Fetch user's answers using the relationship
    user_answers = user.answers
    
    # If user has less than 3 security questions, raise an error
    if len(user_answers) < 3:
        return "Insufficient security questions. Please contact support."

    # Logic to verify user's answers
    correct_answers = 0
    user_answers_dict = {ua.question_id: ua.answer_hash for ua in user.answers}

    print(f"Checking answers for user {user.username}")

    for i in range(3):
        provided_answer = request.form.get(f'security_answer_{i}')
        question_id = request.form.get(f'question_id_{i}')

        print(f"Index: {i}, Question ID: {question_id}, Provided Answer: {provided_answer}")
    
        saved_hash = user_answers_dict.get(int(question_id)) if question_id else None

        if provided_answer and saved_hash:
            match = bcrypt.check_password_hash(saved_hash, provided_answer)
            if match:
                print(f"Answer for question {question_id} matched!")
                correct_answers += 1
            else:
                print(f"Answer for question {question_id} did not match.")
        else:
            print(f"Missing data for question {question_id}. Provided answer: {provided_answer}, Saved hash: {saved_hash}")

    # If all answers are correct, grant access
    if correct_answers == 3:
        return "Access granted."
    return "Access denied."


# Route to handle user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        familyname = request.form.get('familyname')

         # Check if user with provided username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error="Username already exists. Please choose a different username.")
        
        # Fetching available questions
        questions = Question.query.all()
        
        user = User(username=username, name=name, familyname=familyname)        
        db.session.add(user)
        # This will set user.user_id without committing the transaction
        db.session.flush() 

        # Capture user's custom security questions and answers
        for i in range(5): 
            question_text = request.form.get(f'security_question_{i}')
            answer_text = request.form.get(f'security_answer_{i}')
            
            question = Question(question_text=question_text)
            db.session.add(question)
            db.session.flush()

            # Hash the answer before storing
            hashed_answer = bcrypt.generate_password_hash(answer_text).decode('utf-8')
            
            # Store the user's answer in relation to the question
            user_answer = UserAnswer(user_id=user.user_id, question_id=question.question_id, answer_hash=hashed_answer)
            db.session.add(user_answer)
        
        # Commit all database changes
        db.session.commit()
        # Redirect to login after successful registration
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/get_all_questions', methods=['GET'])
def get_all_questions():
    questions = [q.question_text for q in Question.query.all()]
    return jsonify(questions=questions)


# Run the Flask application if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
