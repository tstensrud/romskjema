from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint("auth", __name__)

'''
Log in
'''
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password =  request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Innlogget", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.projects"))
            else:
                flash("Feil i brukernavn eller passord", category="error")
        else:
            flash("Email finnes ikke", category="error")

    return render_template("login.html", user=current_user)


'''
Log out
'''
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))

'''
Sign up
'''
@auth.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        password_confirm = request.form.get('password_re')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("User with email allready exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category="error")
        elif len(name) < 2:
            flash("Name must be longer than 2 characters")
        elif password != password_confirm:
            flash("Passwords does not match")
        else:
            new_user = User(email=email, name = name, password = generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created", category="success")
    
            return redirect(url_for('views.projects'))
    return render_template("sign_up.html", user=current_user)