from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, session, request
from flask_login import login_required, current_user
from .. import models, db
from .. import db_operations as dbo
from ..globals import get_project, pattern_float, pattern_int

rooms_bp = Blueprint('rooms', __name__, static_folder='static', template_folder='templates')

@rooms_bp.route('/', methods=['GET', 'POST'])
@login_required
def rooms():
    project = get_project()
    project_buildings = dbo.get_all_project_buildings(project.id)
    project_rooms = dbo.get_all_project_rooms(project.id)
    project_specification: str = project.Specification
    project_room_types = dbo.get_specification_room_types(project_specification)

    if request.method == "POST":
        building_id = request.form.get("building_id")
        
        if not building_id:
            flash("Feil byggnings-ID", category="error")
            return redirect(url_for("rooms.rooms"))
        building_id = int(building_id)
        
        room_type_id = request.form.get("room_type")
        room_type = dbo.get_room_type_name(project.Specification, room_type_id)
        floor = request.form.get("room_floor").strip()
        name = request.form.get("room_name").strip()
        
        room_number = request.form.get("room_number").strip()
        
        if dbo.check_if_roomnumber_exists(project.id, building_id, room_number):
            flash(f"Romnummer {room_number} finnes allerede for dette bygget", category="error")
            return redirect(url_for("rooms.rooms"))
        
        area = request.form.get("room_area").strip()
        try:
            area = float(area)
        except ValueError:
            flash("Areal kan kun inneholde tall", category="error")
        people = request.form.get("room_people").strip()
        try:
            people = int(people)
        except ValueError:
            flash("Personbelastning kan kun inneholde tall", category="error")
    
        new_room = models.Rooms(BuildingId = building_id,
                                RoomType = room_type_id,
                                Floor = floor,
                                RoomNumber = room_number,
                                RoomName = name,
                                Area = area,
                                RoomPopulation = people)
        db.session.add(new_room)
        try:
            db.session.commit()
        except Exception as e:
            return f"Feil ved oppretting av rom: {e}"
        
        vent_props = dbo.get_room_type_data(room_type_id, project_specification)
        room_ventilation_properties = models.RoomVentilationProperties(RoomId = new_room.id,
                                                                    AirPerPerson=vent_props.air_per_person,
                                                                    AirEmission=vent_props.air_emission,
                                                                    AirProcess=vent_props.air_process,
                                                                    AirMinimum=vent_props.air_minimum,
                                                                    AirSupply = 0.0,
                                                                    AirExtract= 0.0,
                                                                    VentilationPrinciple=vent_props.ventilation_principle,
                                                                    HeatExchange=vent_props.heat_exchange,
                                                                    RoomControl=vent_props.room_control,
                                                                    Notes=vent_props.notes,
                                                                    DbTechnical=vent_props.db_technical,
                                                                    DbNeighbour=vent_props.db_neighbour,
                                                                    DbCorridor=vent_props.db_corridor,
                                                                    Comments=vent_props.comments)
        
        db.session.add(room_ventilation_properties)
        try:
            db.session.commit()
            dbo.initial_ventilation_calculations(new_room.id)
        except Exception as e:
            return f"Feil ved oppretting av ventilation properties {e}"
        return redirect(url_for("rooms.rooms"))
        
    elif request.method == "GET":
        return render_template("rooms.html", 
                            user=current_user, 
                            project=project,
                            project_buildings = project_buildings,
                            project_rooms = project_rooms,
                            project_room_types = project_room_types)

@rooms_bp.route('/update_room', methods=['POST'])
@login_required
def udpate_room():
    if request.method == "POST":
        data = request.get_json()

        room_id = data["room_id"]
        room_number = data["room_number"].strip()
        room_name = data["room_name"].strip()
               
        area = data["area"].strip()
        area_float = pattern_float(area)
        
        population = data["population"].strip()
        population_int = pattern_int(population)
        
        comments = data["comments"].strip()
        
        print(f"ID: {room_id}. rnm: {room_number}. area:{area_float}. rmnm {room_name}, pop: {population_int}, comment: {comments}")
        
        if dbo.update_room_data(room_id, room_number, room_name, area_float, population_int, comments):
            if dbo.update_ventilation_calculations(room_id):
                flash(f"Romdata oppdatert for {room_number}", category="success")
                response = {"success": True, "redirect": url_for("rooms.rooms")}
        else:
            flash("Kunne ikke oppdatere romdata", category="error")
            response = {"success": False}
    
    return jsonify(response)

@rooms_bp.route('/delete_room', methods=['POST'])
@login_required
def delete_room():
    if request.method == "POST":
        data = request.get_json()
        room_id = data["room_id"]
        print(room_id)
        if dbo.delete_room(room_id):
            flash("Rom slettet", category="success")
            response = {"success": True, "redirect": url_for("rooms.rooms")}
        else:
            flash("Kunne ikke slette rom", category="error")
            response = {"success": False}
    return jsonify(response)
