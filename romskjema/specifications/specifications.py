from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_required, current_user
from .. import db_operations as dbo
from ..globals import replace_and_convert_to_float
from markupsafe import escape

specifications_bp = Blueprint('specifications',__name__, static_folder='static', template_folder='templates')

@specifications_bp.route('/', defaults={'specification': None}, methods=['GET', 'POST'])
@specifications_bp.route('/<specification>', methods=['GET', 'POST'])
@login_required
def specifications(specification):
    specifications = dbo.get_specifications()
    if request.method == "GET":
        if specification is None:
            return render_template("specifications.html",
                            user=current_user,
                            specifications=specifications,
                            specification=None)
        else:
            spec_object = dbo.get_specification_by_name(specification)
            specification_data = dbo.get_specification_room_data(specification)
            return render_template("specifications.html",
                                user=current_user,
                                specification=specification,
                                specification_data=specification_data,
                                spec_object = spec_object)

@specifications_bp.route('/new_room', methods=['POST'])
@login_required
def new_room():
    spec = escape(request.form.get("spec"))
    spec_id = escape(request.form.get("spec_id"))
    room_type = escape(request.form.get("room_type"))
    air_per_person = replace_and_convert_to_float(escape(request.form.get("air_per_person")))
    air_emission = replace_and_convert_to_float(escape(request.form.get("air_emission")))
    air_process = replace_and_convert_to_float(escape(request.form.get("air_process")))
    air_minimum = replace_and_convert_to_float(escape(request.form.get("air_minimum")))
    
    if air_per_person is False:
        flash("Luftmengde per person kan kun inneholde tall", category="error")
        return redirect(url_for('specifications.specifications', specification=spec))
    elif air_emission is False:
        flash("Emisjon kan kun inneholde tall", category="error")
        return redirect(url_for('specifications.specifications', specification=spec))
    elif air_process is False:
        flash("Prosess kan kun inneholde tall", category="error")
        return redirect(url_for('specifications.specifications', specification=spec))
    elif air_minimum is False:
        flash("Minimum luftmengde kan kun inneholde tall", category="error")
        return redirect(url_for('specifications.specifications', specification=spec))
    
    vent_principle = escape(request.form.get("ventilation_principle"))
    heat_ex = escape(request.form.get("heat_ex"))
    room_control = escape(request.form.get("room_control"))
    notes = escape(request.form.get("notes"))
    dbtech = escape(request.form.get("db_technical"))
    dbneigh = escape(request.form.get("db_neighbour"))
    dbcorr = escape(request.form.get("db_corridor"))
    comments = escape(request.form.get("comments"))
    if dbo.new_specification_room_type(spec_id, room_type, air_per_person, air_emission, air_process, air_minimum,
                                       vent_principle, heat_ex, room_control, notes, dbtech, dbneigh, dbcorr,
                                       comments):
        flash("Romtype opprettet", category="success")
        
    else:
        flash("Feil i oppretting av romtype", category="error")

    return redirect(url_for('specifications.specifications', specification=spec))

@specifications_bp.route('/new_specification', methods=['GET', 'POST'])
@login_required
def new_specification():
    if request.method == "GET":
        return render_template('new.html',
                            user=current_user,
                            specifications=specifications,
                            specification=None)
    elif request.method == "POST":
        spec_name = escape(request.form.get("spec_name").strip())
        if dbo.find_specification_name(spec_name):
            flash("Spesifikasjon med det navnet finnes allerede", category="error")
            return redirect(url_for('specifications.new_specification'))
        else:
            dbo.new_specifitaion(spec_name)
            return redirect(url_for('specifications.specifications', specification=spec_name))
