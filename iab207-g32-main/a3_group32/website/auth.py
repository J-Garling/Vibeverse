from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint 
auth_bp = Blueprint('auth', __name__)

common_passwords = ['password', '123456', '123456789', 
                    '12345678', '12345', '1234567', 
                    '1234567890', 'password1', '1234', 
                    'qwerty', '123', '123123', 
                    'test', '123321', '123qwe', 
                    '123abc', 'letmein', '111111', 
                    '123456a', 'dragon', '123654', 
                    '654321', '666666', '123123123', 
                    'qwertyuiop', '1q2w3e4r', 'admin']

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name==user_name))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password): 
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') 
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error, 'error')
    return render_template('user.html', form=login_form, heading='Login')

#Registration View Function
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    registration_form = RegisterForm()
    error = None
    if registration_form.validate_on_submit():
        user_name = registration_form.user_name.data
        email = registration_form.email.data
        password = registration_form.password.data
        user = db.session.scalar(db.select(User).where(User.name==user_name))
        if user is not None:
            error = 'User name already exists'
        if len(password) < 8:
            error = 'Password must be at least 8 characters long'
        if password == user_name:
            error = 'Password must be different from user name'
        for common_password in common_passwords:
            if common_password in password:
                error = 'Password is too common'
        if error is None:
            # Create a new user entry in the database
            new_user = User(name = user_name, email = email, password_hash = generate_password_hash(password).decode('utf-8'))
            db.session.add(new_user)
            db.session.commit()
            nextp = request.args.get('next')
            print(nextp)
            # Ensure that the user is redirected to the login page after registration.
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('auth.login'))
            return redirect(nextp)
        else:
            flash(error, 'error')
    return render_template('user.html', form=registration_form, heading='Register')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))