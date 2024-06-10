import os
import json
import re
from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, session, request
from flask_login import login_required, current_user
from . import models, db
from . import db_operations as dbo

views = Blueprint("views", __name__)

def pattern_float(input) -> float:
    pattern = r"\d+(\.\d+)?"
    match = re.search(pattern, input)
    if match:
        return float(match.group())

def pattern_int(input) -> int:
    pattern = r"\d+"
    output = re.findall(pattern, input)
    return int(''.join(output))

@login_required
def get_project():
    project_id = session.get('project_id')
    project = models.Projects.query.get(project_id)
    return project

'''
Views
'''

@views.route('/')
def index():
    return render_template("index.html", 
                           user=current_user, 
                           project=None)

@views.route('/specifications', defaults={'specification': None}, methods=['GET', 'POST'])
@views.route('/specifications/<specification>', methods=['GET', 'POST'])
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
            specification_data = dbo.get_specification_room_data(specification)
            if not specification_data:
                return render_template("specifications.html",
                        user=current_user,
                        specifications=specifications,
                        specification=None)
            else:
                return render_template("specifications.html",
                                    user=current_user,
                                    specification=specification,
                                    specification_data=specification_data)
        
@views.route('/home')
@login_required
def home():
    project = get_project()
    total_area: float = dbo.summarize_project_area(project.id)
    return render_template("home.html", 
                           user=current_user, 
                           project=project, 
                           total_area = total_area)

@views.route('/buildings', methods=['POST', 'GET'])
@login_required
def buildings():
    project = get_project()
   
    if request.method == "GET":
        project_buildings = dbo.get_all_project_buildings(project.id)
        
        building_areas = []
        building_supply = []
        building_extract = []
        for building in project_buildings:
            building_areas.append(dbo.summarize_building_area(project.id, building.id))
            building_supply.append(dbo.summarize_supply_air_building(project.id, building.id))
            building_extract.append(dbo.summarize_extract_air_building(project.id, building.id))

        ziped_building_data = zip(project_buildings, building_areas, building_supply, building_extract)

        return render_template("buildings.html", 
                               user=current_user, 
                               project=project, 
                               project_buildings = ziped_building_data)
   
    elif request.method == "POST":
        building_name = request.form.get("building_name").strip()
        new_building = models.Buildings(ProjectId = project.id, BuildingName = building_name)
        db.session.add(new_building)
        db.session.commit()
        flash(f"Bygg {building_name} opprettet", category="success")
        return redirect(url_for('views.buildings'))
    
@views.route('/rooms', methods=['GET', 'POST'])
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
            return redirect(url_for("views.rooms"))
        building_id = int(building_id)
        
        room_type_id = request.form.get("room_type")
        room_type = dbo.get_room_type_name(project.Specification, room_type_id)
        floor = request.form.get("room_floor").strip()
        name = request.form.get("room_name").strip()
        
        room_number = request.form.get("room_number").strip()
        
        if dbo.check_if_roomnumber_exists(project.id, building_id, room_number):
            flash(f"Romnummer {room_number} finnes allerede for dette bygget", category="error")
            return redirect(url_for("views.rooms"))
        
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
        return redirect(url_for("views.rooms"))
        
    elif request.method == "GET":
        return render_template("rooms.html", 
                            user=current_user, 
                            project=project,
                            project_buildings = project_buildings,
                            project_rooms = project_rooms,
                            project_room_types = project_room_types)

@views.route('/update_room', methods=['POST'])
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
                response = {"success": True, "redirect": url_for("views.rooms")}
        else:
            flash("Kunne ikke oppdatere romdata", category="error")
            response = {"success": False}
    
    return jsonify(response)

@views.route('/delete_room', methods=['POST'])
@login_required
def delete_room():
    if request.method == "POST":
        data = request.get_json()
        room_id = data["room_id"]
        print(room_id)
        if dbo.delete_room(room_id):
            flash("Rom slettet", category="success")
            response = {"success": True, "redirect": url_for("views.rooms")}
        else:
            flash("Kunne ikke slette rom", category="error")
            response = {"success": False}
    return jsonify(response)

@login_required
@views.route('/vent_systems', methods=['GET', 'POST'])
def vent_systems():
    project = get_project()
    if request.method == "POST":
        system_number = request.form.get("system_number").strip()
        if dbo.check_if_system_number_exists(project.id, system_number):
            flash("Systemnummer finnes allerede", category="success")
            return redirect(url_for('views.vent_systems'))
        
        airflow = float(request.form.get("airflow").strip())
        service_area = request.form.get("system_service").strip()
        placement = request.form.get("system_placement").strip()
        system_type = request.form.get("special_system")
        if system_type == None:
            system_type = "Nei"
        else:
            system_type = "Ja"
        system_h_ex = request.form.get("heat_exchange").strip()

        if dbo.new_ventilation_system(project.id, system_number, placement, service_area, system_h_ex, airflow, system_type):
            flash("System opprettet", category="success")
            return redirect(url_for('views.vent_systems'))
        else:
            flash("Kunne ikke opprette system.", category="error")
            return redirect(url_for('views.vent_systems'))
    
    if request.method == "GET":
        systems = dbo.get_all_systems(project.id)
        return render_template("vent_systems.html", 
                            user=current_user, 
                            project=project,
                            systems=systems)

@login_required
@views.route('/update_system', methods=['POST'])
def update_system():
    data = request.get_json()
    system_id = data["system_id"]
    system_number = data["system_number"].strip()   
    system_location = data["system_location"].strip()
    service_area = data["service_area"].strip()
    airflow = data["airflow"].strip()
    airflow_float = pattern_float(airflow)
    heat_ex = data["system_hx"].strip()
    
    if dbo.update_system_info(system_id, system_number, system_location, service_area, airflow_float, heat_ex):
        flash("System-data oppdatert", category="success")
        response = {"success": True, "redirect": url_for("views.vent_systems")}
    else:
        flash("Kunne ikke oppdatere system-data", category="error")
        response = {"success": False, "redirect": url_for("views.vent_systems")}
    
    return jsonify(response)


@views.route('/ventilation', defaults={'building_id': None}, methods=['GET', 'POST'])
@views.route('/ventilation/<building_id>', methods=['GET', 'POST'])
@login_required
def ventilation(building_id):
    project = get_project()

    if request.method == "POST":       
        # Showing specific buildings in the table
        requested_building_id = request.form.get("project_building")
        if requested_building_id != "none" and requested_building_id != "showall":
            return redirect(url_for("views.ventilation", building_id = requested_building_id))
        else:
            return redirect(url_for("views.ventilation", building_id = "showall"))
    
    elif request.method == "GET":
        # Show all rooms for building
        if building_id is not None and building_id != "showall":
            ventilation_data = dbo.get_ventilation_data_rooms_in_building(project.id, building_id)
        # Show all rooms for project
        else:
            ventilation_data = dbo.get_ventlation_data_all_rooms_project(project.id)
        project_buildings = dbo.get_all_project_buildings(project.id)
        systems = dbo.get_all_systems(project.id)
        
        return render_template("ventilation.html",
                               user=current_user,
                               project=project,
                               ventilation_data = ventilation_data,
                               project_buildings = project_buildings,
                               system_names = systems)

@views.route('/update_ventilation', methods=['POST'])
@login_required
def update_ventilation():    
    data = request.get_json()

    # If system is updated
    if data["system_update"] == True:
        old_system_id = data["old_system_id"]
        system_id = data["system_id"]
        vent_prop_id = data["row_id"]
        
        if old_system_id == "none":
            response = {"success": True, "redirect": url_for("views.ventilation")}

        if old_system_id == system_id:
            if dbo.update_system_airflows(system_id):
                flash("System oppdatert", category="success")
                response = {"success": True, "redirect": url_for("views.ventilation")}
            else:
                flash("Kunne ikke oppdatere luftmengde dbo.update_system_airflows", category="error")
                response = {"success": False, "redirect": url_for("views.ventilation")}
        else:
            dbo.set_system_for_room_vent_prop(vent_prop_id, system_id)
            if dbo.update_airflow_changed_system(system_id, old_system_id):
                flash("System oppdatert", category="success")
                response = {"success": True, "redirect": url_for("views.ventilation")}
            else:
                flash("Kunne ikke oppdatere luftmengder: update_airflow_changed_system", category="error")
                response = {"success": False, "redirect": url_for("views.ventilation")}
        return jsonify(response)




    
    vent_prop_id = data["vent_data_id"]
    supply = data["supply_air"].strip()
    new_supply = pattern_float(supply)
    extract = data["extract_air"].strip()
    new_extract = pattern_float(extract)
    comment = data["comment"].strip()

    if dbo.update_ventilation_table(vent_prop_id, new_supply, new_extract, None, comment):
        flash("Data oppdatert", category="success")
        response = {"success": True, "redirect": url_for("views.ventilation")}
    else:
        flash("Kunne ikke oppdatere verdier.", category="error")
        response = {"success": False, "redirect": url_for("views.ventilation")}
    return jsonify(response)


@views.route('/change_project', methods=['GET', 'POST'])
@login_required
def change_project():
    project_name = request.form.get('project_name')
    if project_name:
        project_object = models.Projects.query.filter_by(ProjectName=project_name).first()
        project_id = project_object.id
        session['project_id'] = project_id
        return redirect(url_for('views.home'))

@views.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == "GET":
        return render_template("new_project.html",
                               user=current_user)
    elif request.method == "POST":
        project_name = request.form.get('project_name').strip()
        project_number = request.form.get('project_number').strip()
        project_description = request.form.get('project_description').strip()
                
        if dbo.check_for_existing_project_number(project_number):
            flash("Prosjektnummer finnes allerede", category="error")
            return redirect(url_for("views.project"))
        
        new_project = models.Projects(ProjectNumber=project_number, 
                                      ProjectName=project_name, 
                                      ProjectDescription=project_description, 
                                      Specification=None)
        try:
            db.session.add(new_project)
            db.session.commit()
        except Exception as e:
            flash(f"Kunne ikke opprette prosjekt: {e}", category="error")
            return redirect(url_for("views.project"))
        
        session['project_name'] = project_name
        flash(f"Prosjekt \"{project_name}\" er opprettet", category="success")
        return redirect(url_for('views.projects'))

@views.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():    
    if request.method == "POST":
        # Project selected from /projects drop down
        project_id = request.form.get('project_id')
        if project_id:
            session['project_id'] = project_id
            return redirect(url_for('views.home'))
        
    elif request.method == "GET":
        projects = dbo.get_all_projects()
        return render_template("projects.html",
                               user=current_user,
                               projects=projects,
                               project=None)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    project = get_project()
    specifications = dbo.get_specifications()
    if request.method == "GET":
        return render_template("settings.html",
                            user = current_user,
                            project = project,
                            specifications = specifications)
    elif request.method == "POST":
        new_project_number = request.form.get("project_number").strip()
        new_project_name = request.form.get("project_name").strip()
        new_project_description = request.form.get("project_description")
        new_specification_id = request.form.get("project_specification")
        if new_specification_id == "none":
            pass
        else:    
            specification = models.Specifications.query.filter_by(id=new_specification_id).first()
            project.Specification = specification.name
        
        project.ProjectNumber = new_project_number
        project.ProjectName = new_project_name
        project.ProjectDescription = new_project_description
        

        db.session.commit()
        return redirect(url_for('views.home'))


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
    
    json_file_path = os.path.join(os.path.dirname(__file__), "static", f"specifications\skok.json")
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


