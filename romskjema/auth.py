from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from markupsafe import escape

auth = Blueprint("auth", __name__)

'''
Log in
'''
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = escape(request.form.get('email'))
        password =  escape(request.form.get('password'))

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                #user.logged_in = True
                #db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("projects.projects_dashboard"))
            else:
                flash("Feil i brukernavn eller passord", category="error")
        else:
            flash("Email finnes ikke", category="error")
    flash("Kunne ikke logge inn", category="error")
    return render_template("index.html", user=current_user)


'''
Log out
'''
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))

'''
Sign up for testing
'''
@auth.route('/initialize', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            new_user = User(email=email, name = name, password = generate_password_hash(password, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created", category="success")
            return redirect(url_for('projects.projects_dashboard'))
        
    if request.method == "GET":
        email = "admin@admin.com"
        name = "Administrator"
        password = "1234"
        user = User.query.filter_by(email=email).first()
        if not user:
            admin_account = User(email=email, name=name, password = generate_password_hash(password, method='scrypt'), logged_in=False, admin=True, is_active=True)
            db.session.add(admin_account)
            db.session.commit()
            login_user(admin_account, remember=True)
            return redirect(url_for('projects.projects_dashboard'))
        else:
            return redirect(url_for('projects.projects_dashboard'))