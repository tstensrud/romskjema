from flask import Blueprint, session, redirect, url_for, request, render_template, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_
from . import models, db
from . import db_operations as dbo

views = Blueprint("views", __name__)

'''
Non views methods
'''
@login_required
def get_project():
    project_id = session.get('project_id')
    project = models.Projects.query.get(project_id)
    return project

@login_required
def get_all_project_names():
    project_names = []
    projects = models.Projects.query.all()
    for project_name in projects:
        project_names.append(project_name.ProjectName)
    return project_names

@login_required
def get_specifications():
    spec_list = []
    specifications = models.Specifications.query.all()
    for spec in specifications:
        spec_list.append(spec)
    return spec_list

@login_required
def get_specification_room_types(specification: str):
    room_types = db.session.query(models.RoomTypes).join(models.Specifications).filter(models.Specifications.name == specification).all()
    return room_types

@login_required
def get_room_type_data(room_type_id: int):
    room_data_object = db.session.query(models.RoomDataVentilation).join(models.RoomTypes).filter(models.RoomTypes.id == room_type_id).first()
    return room_data_object


'''
Views
'''

@views.route('/')
def index():
    return render_template("index.html", 
                           user=current_user, 
                           project=None)

@views.route('/home')
@login_required
def home():
    project = get_project()
    project_names = get_all_project_names()
    total_area = dbo.summarize_project_area(project.id)
    return render_template("home.html", 
                           user=current_user, 
                           project=project, 
                           project_names=project_names,
                           total_area = total_area)

@views.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
    project = get_project()
    project_names = get_all_project_names()
    project_buildings = db.session.query(models.Buildings).filter(models.Buildings.ProjectId == project.id).all()
    project_rooms = db.session.query(models.Rooms).join(models.Buildings).join(models.Projects).filter(models.Projects.id == project.id).order_by(models.Buildings.BuildingName, models.Rooms.Floor).all()
    project_specification: str = project.Specification
    project_room_types = get_specification_room_types(project_specification)

    if request.method == "POST":
        building_id = request.form.get("building_id")
        
        if not building_id:
            flash("Feil byggnings-ID", category="error")
            return redirect(url_for("views.rooms"))
        building_id = int(building_id)
        
        room_type_id = request.form.get("room_type")
        floor = request.form.get("room_floor").strip()
        name = request.form.get("room_name").strip()
        
        room_number = request.form.get("room_number").strip()
        existing_room_number = db.session.query(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project.id, models.Buildings.id == building_id, models.Rooms.RoomNumber == room_number)).first()
        if existing_room_number:
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
        
        vent_props = get_room_type_data(room_type_id)
        room_ventilation_properties = models.VentilationProperties(RoomId = new_room.id,
                                                                    area = new_room.Area,
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
                                                                    DBCorridor=vent_props.db_corridor,
                                                                    Comments=vent_props.comments)
        
        db.session.add(room_ventilation_properties)
        try:
            db.session.commit()
            dbo.initial_ventilation_calculations(project.id, building_id, new_room.id)
        except Exception as e:
            return f"Feil ved oppretting av ventilation properties {e}"
        return redirect(url_for("views.rooms"))
        
    elif request.method == "GET":
        return render_template("rooms.html", 
                            user=current_user, 
                            project=project, 
                            project_names=project_names,
                            project_buildings = project_buildings,
                            project_rooms = project_rooms,
                            project_room_types = project_room_types)

@views.route('/update_room', methods=['POST'])
@login_required
def update_room():
    data = request.get_json()

@views.route('/update_ventilation', methods=['POST'])
@login_required
def update_ventilation():
    data = request.get_json()

@views.route('/ventilation', defaults={'building_id': None}, methods=['GET', 'POST'])
@views.route('/ventilation/<building_id>', methods=['GET', 'POST'])
@login_required
def ventilation(building_id):
    project = get_project()
    project_names = get_all_project_names()

    if request.method == "POST":
        
        # Showing specific buildings in the table
        requested_building_id = request.form.get("project_building")
        if requested_building_id != "none" and requested_building_id != "showall":
            return redirect(url_for("views.ventilation", building_id = requested_building_id))
        else:
            return redirect(url_for("views.ventilation", building_id = "showall"))
    
    elif request.method == "GET":
        if building_id is not None and building_id != "showall":
            ventilation_data = db.session.query(models.VentilationProperties).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project.id, models.Buildings.id == building_id)).order_by(models.Rooms.Floor).all()    
        else:
            ventilation_data = db.session.query(models.VentilationProperties).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(models.Projects.id == project.id).order_by(models.Buildings.BuildingName, models.Rooms.Floor).all()
        
        project_buildings = db.session.query(models.Buildings).join(models.Projects).filter(models.Projects.id == project.id).all()
        return render_template("ventilation.html",
                               user=current_user,
                               project=project,
                               project_names=project_names,
                               ventilation_data = ventilation_data,
                               project_buildings = project_buildings)

@views.route('/change_project', methods=['GET', 'POST'])
@login_required
def change_project():
    project_name = request.form.get('project_name')
    if project_name:
        project_object = models.Projects.query.filter_by(ProjectName=project_name).first()
        project_id = project_object.id
        session['project_id'] = project_id
        print(session['project_name'])
        return redirect(url_for('views.home'))

@views.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():    
    if request.method == "POST":
        # Project selected from /projects drop down
        project_id = request.form.get('project_id')
        if project_id:
            session['project_id'] = project_id
            return redirect(url_for('views.home'))

        # If creating new project
        project_name = request.form.get('project_name')
        project_number = request.form.get('project_number')
        project_description = request.form.get('project_description')
        project = models.Projects.query.filter_by(ProjectNumber = project_number).first()
        
        if project:
            flash("Prosjektnummer finnes allerede", category="error")
        elif len(project_name) <= 1:
            flash("Prosjektnavn er for kort")
        
        new_project = models.Projects(ProjectNumber=project_number, 
                                      ProjectName=project_name, 
                                      ProjectDescription=project_description, 
                                      Specification=None)
        db.session.add(new_project)
        db.session.commit()
        session['project_name'] = project_name
        flash(f"Prosjekt \"{project_name}\" er opprettet", category="success")
        return redirect(url_for('views.projects'))
        
    elif request.method == "GET":
        projects = models.Projects.query.all()
        return render_template("projects.html", user=current_user, projects=projects, project=None)

@views.route('/buildings', methods=['POST', 'GET'])
@login_required
def buildings():
    project = get_project()
    project_names = get_all_project_names()
   
    if request.method == "GET":
        project_buildings = models.Buildings.query.filter_by(ProjectId = project.id).all()
        
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
                               project_names=project_names, 
                               project_buildings = ziped_building_data)
   
    elif request.method == "POST":
        building_name = request.form.get("building_name")
        new_building = models.Buildings(ProjectId = project.id, BuildingName = building_name)
        db.session.add(new_building)
        db.session.commit()
        flash(f"Bygg {building_name} opprettet", category="success")
        return redirect(url_for('views.buildings'))

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    project = get_project()
    project_names = get_all_project_names()
    specifications = get_specifications()
    if request.method == "GET":
        return render_template("settings.html",
                            user = current_user,
                            project = project,
                            project_names = project_names,
                            specifications = specifications)
    elif request.method == "POST":
        new_project_number = request.form.get("project_number")
        new_project_name = request.form.get("project_name")
        new_project_description = request.form.get("project_description")
        new_specification_id = request.form.get("project_specification")
        specification = models.Specifications.query.filter_by(id=new_specification_id).first()

        project.ProjectNumber = new_project_number
        project.ProjectName = new_project_name
        project.ProjectDescription = new_project_description
        project.Specification = specification.name

        db.session.commit()
        return redirect(url_for('views.home'))

@views.route("/settings/customspecification", methods=['POST'])
@login_required
def custom_specification():
    pass




'''
For testing purposes
'''

""" @views.route("/spec_setup")
def spec_setup():
    name = "skok"
    spec = models.Specifications(name=name)
    db.session.add(spec)
    try:
        db.session.commit()
        return f"{name} created"
    except Exception as e:
        return f"Could not create {name}, {e}" """


""" @views.route("/spec_rooms_setup")
def spec_rooms_setup():
    spec_name = "skok"
    spec = models.Specifications.query.filter_by(name=spec_name).first()
    
    room = models.RoomTypes(specification_id=spec.id,
                                name="Korridor")
    try:
        db.session.add(room)
        db.session.commit()
    except Exception as e:
        return f"Failed {e}"  
    
    ventprops = models.RoomDataVentilation(room_type_id = room.id,
                                           air_per_person = 0,
                                           air_emission = 7.2,
                                           air_process = 0,
                                           air_minimum = 3.6,
                                           ventilation_principle = "Omrøring",
                                           heat_exchange = "R",
                                           room_control = "V,T,CO2,B",
                                           notes = "",
                                           db_technical = "33dBA",
                                           db_neighbour = "",
                                           db_corridor = "",
                                           comments = "")
    try:
        db.session.add(ventprops)
        db.session.commit()
    except Exception as e:
        return f"Failed {e}"
    
    return f"Created type {room.name} linked to spec: {spec.name} id: {spec.id}. VentproID {ventprops.id}"   """  

""" @views.route("/clear")
def clear():
    db.session.query(models.RoomTypes).delete()
    db.session.commit()
    return f"Deleted all entries" """


