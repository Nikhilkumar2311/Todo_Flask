from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "TODO"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Table(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.username}"


# initialize the database
with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Table.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
        return redirect(url_for('home'))


@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = Table.query.filter_by(username=username).first()
        if user and user.password == password:
            return "Login Successful"
        else:
            return "Invalid username or password"
    return render_template('home.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        iusername = request.form.get("username")
        ipassword = request.form.get("password")
        icpassword = request.form.get("cpassword")
        user = Table.query.filter_by(username=iusername).first()
        if user:
            flash('User already exists')
            return render_template('signup.html')
        if len(ipassword) < 8:
            flash('Password should contain atleast 8 Characters')
            return render_template('signup.html')
        if ipassword.isdigit():
            flash('Password should contain One Uppercase and One LowerCase')
            return render_template('signup.html')
        if ipassword.islower():
            flash('Password should contain One Uppercase and One Digit')
            return render_template('signup.html')
        if ipassword.isupper():
            flash('Password should contain One Digit and One LowerCase')
            return render_template('signup.html')
        if ipassword != icpassword:
            flash('Password does not match')
            return render_template('signup.html')
        user = Table(username=iusername, password=generate_password_hash(ipassword, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        print(user)
        return render_template('login.html')
    return render_template('signup.html')


if __name__ == "__main__":
    app.run(debug=True)