import os
import json
from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_user, current_user, login_required
from . import models, db

views = Blueprint("views", __name__)

'''
Views
'''

@views.route('/')
def index():
        if current_user.is_authenticated:
            return redirect(url_for('projects.projects'))
        else:
            return render_template("index.html", 
                                user=current_user, 
                                project=None)

@views.route('/initialize', methods=['GET'])
def initialize():
        
    email = "admin@admin.com"
    name = "Administrator"
    password = "1234"
    user = models.User.query.filter_by(email=email).first()
    if not user:
        admin_account = models.User(email=email, name=name, password = generate_password_hash(password, method='scrypt'), logged_in=False, admin=True, is_active=True)
        db.session.add(admin_account)
        db.session.commit()
        if spec_rooms_setup():
            login_user(admin_account, remember=True)
        else:
            return "Failed to initialize"
        return redirect(url_for('projects.projects'))
    else:
        return redirect(url_for('projects.projects'))

'''
Set up default specifications
'''
def spec_rooms_setup() -> bool:

    names = ["Skok skoler 2022-o2023", "Skok flerbrukshaller 2022-o2023"]
    
    for name in names:
        spec = models.Specifications(name=name)
        db.session.add(spec)
        try:
            db.session.commit()
        except Exception as e:
            return f"Could not create {name}, {e}"

    
        spec = models.Specifications.query.filter_by(name=name).first()
        
        json_file_path = os.path.join(os.path.dirname(__file__), "static", f"specifications/{name}.json")
        with open(json_file_path, encoding="utf-8") as jfile:
            data = json.load(jfile)

        
        for key, value in data.items():
            key = key.capitalize()
            key = key.replace("_", " ")
            values = []
            for _, value in value.items():
                values.append(value)
            room = models.RoomTypes(specification_id=spec.id,
                                    name=key,
                                    air_per_person = values[0],
                                    air_emission = values[1],
                                    air_process = values[2],
                                    air_minimum = values[3],
                                    ventilation_principle = values[4],
                                    heat_exchange = values[5],
                                    room_control = values[6],
                                    notes = values[7],
                                    db_technical = values[8],
                                    db_neighbour= values[9],
                                    db_corridor = values[10],
                                    comments = values[11])
            try:
                db.session.add(room)
                db.session.commit()
            except Exception as e:
                return False
    
    return True


