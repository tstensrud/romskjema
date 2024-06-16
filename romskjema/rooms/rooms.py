from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, session, request
from flask_login import login_required, current_user
from .. import db_operations as dbo
from .. import db_ops_heating as dboh
from ..globals import get_project, pattern_float, pattern_int
from markupsafe import escape

rooms_bp = Blueprint('rooms', __name__, static_folder='static', template_folder='templates')

@rooms_bp.route('/', methods=['GET', 'POST'])
@login_required
def rooms(project_id):
    project = dbo.get_project(project_id)
    endpoint = request.endpoint
    project_buildings = dbo.get_all_project_buildings(project.id)
    project_rooms = dbo.get_all_project_rooms(project.id)
    project_specification: str = project.Specification
    project_room_types = dbo.get_specification_room_types(project_specification)

    if request.method == "POST":
        building_id = request.form.get("building_id")
        
        if not building_id:
            flash("Feil byggnings-ID", category="error")
            return redirect(url_for("rooms.rooms", project_id = project.id))
        building_id = int(building_id)
        
        room_type_id = escape(request.form.get("room_type"))
        room_type = dbo.get_room_type_name(project.Specification, room_type_id)
        floor = escape(request.form.get("room_floor").strip())
        name = escape(request.form.get("room_name").strip())
        
        room_number = escape(request.form.get("room_number").strip())
        
        if dbo.check_if_roomnumber_exists(project.id, building_id, room_number):
            flash(f"Romnummer {room_number} finnes allerede for dette bygget", category="error")
            return redirect(url_for("rooms.rooms", project_id = project.id))
        
        area = escape(request.form.get("room_area").strip())
        try:
            area = float(area)
        except ValueError:
            flash("Areal kan kun inneholde tall", category="error")
            return redirect(url_for("rooms.rooms", project_id=project_id))
            
        people = escape(request.form.get("room_people").strip())
        try:
            people = int(people)
        except ValueError:
            flash("Personbelastning kan kun inneholde tall", category="error")
            return redirect(url_for("rooms.rooms", project_id=project_id))
    
        new_room_id = dbo.new_room(building_id, room_type_id, floor, room_number, name, area, people)

        # Check if creating room was OK
        if new_room_id is not False:
            vent_props = dbo.get_room_type_data(room_type_id, project_specification)

            # Create row for room vent props
            if dbo.new_vent_prop_room(new_room_id, vent_props.air_per_person, vent_props.air_emission,
                                   vent_props.air_process, vent_props.air_minimum,
                                   vent_props.ventilation_principle, vent_props.heat_exchange,
                                   vent_props.room_control, vent_props.notes, vent_props.db_technical,
                                   vent_props.db_neighbour, vent_props.db_corridor, vent_props.comments):
                dbo.initial_ventilation_calculations(new_room_id)
                building_heating_settings = dboh.get_building_heating_settings(building_id)
                
                # Create row for room heating props
                if dboh.new_room_heating_props(building_heating_settings.id, new_room_id):
                    flash("Rom opprettet", category="success")
                    return redirect(url_for("rooms.rooms", project_id = project.id))
                else:
                    flash("Feil ved oppretting av rom heating props", category="error")
                    return redirect(url_for("rooms.rooms", project_id = project.id))
        
    elif request.method == "GET":
        return render_template("rooms.html", 
                            user=current_user, 
                            project=project,
                            project_buildings = project_buildings,
                            project_rooms = project_rooms,
                            project_room_types = project_room_types,
                            endpoint=endpoint,
                            project_id = project_id)

@rooms_bp.route('/update_room', methods=['POST'])
@login_required
def udpate_room(project_id):
    if request.method == "POST":
        data = request.get_json()
        project_id = escape(data["project_id"])
        room_id = escape(data["room_id"])
        room_number = escape(data["room_number"].strip())
        room_name = escape(data["room_name"].strip())
               
        area = escape(data["area"].strip())
        area_float = pattern_float(area)
        
        population = escape(data["population"].strip())
        population_int = pattern_int(population)
        
        comments = escape(data["comments"].strip())
        
        #print(f"ID: {room_id}. rnm: {room_number}. area:{area_float}. rmnm {room_name}, pop: {population_int}, comment: {comments}")
        
        if dbo.update_room_data(room_id, room_number, room_name, area_float, population_int, comments):
            if dbo.update_ventilation_calculations(room_id):
                flash(f"Romdata oppdatert for {room_number}", category="success")
                response = {"success": True, "redirect": url_for("rooms.rooms", project_id = project_id)}
        else:
            flash("Kunne ikke oppdatere romdata", category="error")
            response = {"success": False}
    
    return jsonify(response)

@rooms_bp.route('/delete_room', methods=['POST'])
@login_required
def delete_room(project_id):
    if request.method == "POST":
        data = request.get_json()
        room_id = escape(data["room_id"])
        print(room_id)
        if dbo.delete_room(room_id):
            flash("Rom slettet", category="success")
            response = {"success": True, "redirect": url_for("rooms.rooms", project_id = project_id)}
        else:
            flash("Kunne ikke slette rom", category="error")
            response = {"success": False}
    return jsonify(response)
