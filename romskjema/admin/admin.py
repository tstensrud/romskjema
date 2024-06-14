from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_required, current_user
from .. import models, db
from .. import db_ops_admin as dboa
from werkzeug.security import generate_password_hash
from functools import wraps
from markupsafe import escape
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

admin_bp = Blueprint('admin', __name__, template_folder="templates", static_folder="static")

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.admin:
            print("Unauthorized attempt")
        return f(*args, **kwargs)
    return decorated_function

@login_required
def send_user_email(subject: str, body: str, to_email: str) -> None:
    from_email = "structortsit@gmail.com"
    password = "uVgvJarREQ5V7L"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg = MIMEText(body)

    with smtplib.SMTP_SSL('smtp.gmail.com') as smtp_server:
        smtp_server.login(from_email, password)
        smtp_server.sendmail(from_email, to_email, msg.as_string())
        

    



@login_required
def get_users():
    users = db.session.query(models.User).all()
    return users


@login_required
@admin_required
@admin_bp.route('/', methods=['GET', 'POST'])
def admin():
    if request.method == "GET":
        users = get_users()
        return render_template("admin.html",
                            user=current_user,
                            users=users)
    elif request.method == "POST":
        pass

@login_required
@admin_required
@admin_bp.route('/new_user', methods=['POST'])
def new_user():
    
    email = escape(request.form.get("email").strip())
    name = escape(request.form.get("name").strip())
    password = escape(request.form.get("password").strip())
    

    if dboa.find_existing_user(email):
        flash("Email allerede registrert", category="error")
    else:
        new_user = models.User(email=email, name=name, password=generate_password_hash(password, method='scrypt'))
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            flash("Kunne ikke opprette bruker", category="error")
    subject = "Konto opprettet"
    body = f"Din nye brukerkonto hos Structor TS IT er opprettet. \n Brukernavn er {email}.\n Passord: {password}"
    send_user_email(subject, body, email)


    return redirect(url_for("admin.admin"))
