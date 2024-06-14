from flask import Blueprint, redirect, url_for, render_template, flash, request, session
from flask_login import login_required, current_user
from .. import models, db
from .. import db_operations as dbo
from ..globals import get_project

projects_bp = Blueprint('projects', __name__, static_folder='static', template_folder='templates')

@projects_bp.route('/')
@login_required
def projects():
    project = get_project()
    if project != "none" and project is not None:
        total_area: float = dbo.summarize_project_area(project.id)
        return render_template("home.html", 
                            user=current_user, 
                            project=project, 
                            total_area = total_area)
    else:
        return redirect(url_for("projects.projects_dashboard"))

@projects_bp.route('/settings', methods=['GET', 'POST'])
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
        return redirect(url_for('projects.settings'))
 
@projects_bp.route('/change_project', methods=['GET', 'POST'])
@login_required
def change_project():
    project_name = request.form.get('project_name')
    if project_name:
        project_object = models.Projects.query.filter_by(ProjectName=project_name).first()
        project_id = project_object.id
        session['project_id'] = project_id
        return redirect(url_for('views.home'))

@projects_bp.route('/new_project', methods=['GET', 'POST'])
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
            return redirect(url_for("projects.project"))
        
        new_project = models.Projects(ProjectNumber=project_number, 
                                      ProjectName=project_name, 
                                      ProjectDescription=project_description, 
                                      Specification=None)
        try:
            db.session.add(new_project)
            db.session.commit()
        except Exception as e:
            flash(f"Kunne ikke opprette prosjekt: {e}", category="error")
            return redirect(url_for("projects.project"))
        
        session['project_name'] = project_name
        flash(f"Prosjekt \"{project_name}\" er opprettet", category="success")
        return redirect(url_for('projects.projects'))

@projects_bp.route('/projects_dashboard', methods=['GET', 'POST'])
@login_required
def projects_dashboard():    
    if request.method == "POST":
        
        project_id = request.form.get('project_id')
        if project_id:
            session['project_id'] = project_id
            return redirect(url_for('projects.projects'))
        else:
            return redirect(url_for('projects.projects.projects_dashboard'))
        
    elif request.method == "GET":
        projects = dbo.get_all_projects()
        return render_template("projects.html",
                               user=current_user,
                               projects=projects,
                               project=None)


