from flask import Blueprint, session, redirect, url_for, request, render_template, flash, jsonify
from flask_login import login_required, current_user
from . import models, db

views = Blueprint("views", __name__)

'''
Non views methods
'''
@login_required
def get_all_project_names():
    project_names = []
    projects = models.Projects.query.all()
    for project_name in projects:
        project_names.append(project_name.ProjectName)
    return project_names

# Get project object of current session variable 'project_id'
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

@views.route('/home')
@login_required
def home():
    project = get_project()
    project_names = get_all_project_names()
    return render_template("home.html", 
                           user=current_user, 
                           project=project, 
                           project_names=project_names)

@views.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
    project = get_project()
    project_names = get_all_project_names()
    project_buildings = db.session.query(models.Buildings).filter(models.Buildings.ProjectId == project.id).all()
    project_rooms = db.session.query(models.Rooms).join(models.Buildings).join(models.Projects).filter(models.Projects.id == project.id).all()
    
    if request.method == "POST":
        building_id = request.form.get("building_id")
        print(f"Building ID: {building_id}")
        if not building_id:
            flash("Feil byggnings-ID", category="error")
            return redirect(url_for("views.rooms"))
        building_id = int(building_id)
        
        room_type = request.form.get("room_type")
        floor = request.form.get("room_floor")
        name = request.form.get("room_name")
        number = request.form.get("room_number")
        area = request.form.get("room_area")
        try:
            area = float(area)
        except ValueError:
            flash("Areal kan kun inneholde tall", category="error")
        people = request.form.get("room_people")
        try:
            people = int(people)
        except ValueError:
            flash("Personbelastning kan kun inneholde tall", category="error")
        if building_id != "none":
            new_room = models.Rooms(BuildingId = building_id,
                                    RoomType = room_type,
                                    Floor = floor,
                                    RoomNumber = number,
                                    RoomName = name,
                                    Area = area,
                                    RoomPopulation = people)
            db.session.add(new_room)
            db.session.commit()
            print(f"Room {number} added")
            return redirect(url_for("views.rooms"))
        
    elif request.method == "GET":
        return render_template("rooms.html", 
                            user=current_user, 
                            project=project, 
                            project_names=project_names,
                            project_buildings = project_buildings,
                            project_rooms = project_rooms)

@views.route('/update_room', methods=['POST'])
@login_required
def update_room():
    data = request.get_json()

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
        project_spec = request.form.get('project_specification')
        project = models.Projects.query.filter_by(ProjectNumber = project_number).first()
        
        if project:
            flash("Prosjektnummer finnes allerede", category="error")
        elif len(project_name) <= 1:
            flash("Prosjektnavn er for kort")
        
        new_project = models.Projects(ProjectNumber=project_number, 
                                      ProjectName=project_name, 
                                      ProjectDescription=project_description, 
                                      Specification=project_spec)
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
        print(project_buildings)
        return render_template("buildings.html", 
                               user=current_user, 
                               project=project, 
                               project_names=project_names, 
                               project_buildings = project_buildings)
   
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
    if request.method == "GET":
        return render_template("settings.html",
                            user = current_user,
                            project = project,
                            project_names = project_names)
    elif request.method == "POST":
        new_project_number = request.form.get("project_number")
        new_project_name = request.form.get("project_name")
        new_project_description = request.form.get("project_description")

        project.ProjectNumber = new_project_number
        project.ProjectName = new_project_name
        project.ProjectDescription = new_project_description

        db.session.commit()
        return redirect(url_for('views.home'))

