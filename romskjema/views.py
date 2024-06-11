import os
import json
from flask import Blueprint, render_template
from flask_login import current_user
from . import models, db
from . import db_operations as dbo

views = Blueprint("views", __name__)

'''
Views
'''
@views.route('/')
def index():
    return render_template("index.html", 
                           user=current_user, 
                           project=None)


'''
For testing purposes
'''
@views.route("/spec_rooms_setup")
def spec_rooms_setup():

    name = "skok"
    spec = models.Specifications(name=name)
    db.session.add(spec)
    try:
        db.session.commit()
    except Exception as e:
        return f"Could not create {name}, {e}"

    spec_name = "skok"
    spec = models.Specifications.query.filter_by(name=spec_name).first()
    
    json_file_path = os.path.join(os.path.dirname(__file__), "static", f"specifications/skok.json")
    with open(json_file_path, encoding="utf-8") as jfile:
        data = json.load(jfile)

    
    for parent_key, nested_dict in data.items():
        parent_key = parent_key.capitalize()
        parent_key = parent_key.replace("_", " ")
        values = []
        for _, value in nested_dict.items():
            values.append(value)
        room = models.RoomTypes(specification_id=spec.id,
                                name=parent_key,
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
            return f"Failed to create room {e}"
    
    return f"Rooms created"


