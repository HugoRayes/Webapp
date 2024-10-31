from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create the website
app = Flask(__name__)

# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church.db'
db = SQLAlchemy(app)

# Create the Member table in database
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

# Home page
@app.route('/')
def home():
    return render_template('home.html')

# Show all members
@app.route('/members')
def members():
    all_members = Member.query.all()
    return render_template('members.html', members=all_members)

# Add new member
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        new_member = Member(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone']
        )
        db.session.add(new_member)
        db.session.commit()
        return redirect('/members')
    return render_template('add_member.html')

# Start the website
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)