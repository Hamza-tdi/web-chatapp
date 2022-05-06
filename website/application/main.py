from flask import Flask, render_template, url_for, session, redirect, flash
from flask_socketio import SocketIO, send
from wtf_forms import *
from models import *

from passlib.hash import pbkdf2_sha256
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

NAME_KEY = 'name'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'v6sdv46sfé6zd4f6zfz56vcz6v4z6v5zv65dsv'
socketio = SocketIO(app)


# DATA BASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://acseqcoypnjqmm:4b58b87a33ef4ce72ce10a0674b0a92ca0ed1c317f5326a5904f793cf4fd3a22@ec2-52-203-118-49.compute-1.amazonaws.com:5432/db7jrfrq7nv50n'
db = SQLAlchemy(app)


# Configure flask login
login = LoginManager(app)
login.init_app(app)


@login.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out', 'success')
    return render_template(url_for('login'))


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html', username=current_user.username)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_authenticated:
        flash('Please login.', 'danger')
        return redirect(url_for('login'))

    return render_template('dashboard.html')


@app.route('/register',  methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        hashed_pswd = pbkdf2_sha256.hash(password)

        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)


@app.route('/',  methods=['GET', 'POST'])
@app.route('/login')
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        if current_user.is_authenticated:
            flash('You are logged in', 'success')
            return redirect(url_for('dashboard'))

        return 'Not logged in'

    return render_template('login.html', form=login_form)


@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send(data)


@socketio.on('connect')
def connect(data):
    print(f"\n\n{data}\n\n")


if __name__ == '__main__':
    socketio.run(app, debug=True)
