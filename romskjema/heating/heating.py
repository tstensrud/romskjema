from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, session, request
from flask_login import login_required, current_user
from .. import models, db
from .. import db_operations as dbo
from .. import db_ops_heating as dboh
from ..globals import get_project, pattern_float, pattern_int
from markupsafe import escape

heating_bp = Blueprint('heating', __name__, static_folder="static", template_folder="templates")


@heating_bp.route('/', defaults={'building': None}, methods=['GET', 'POST'])
@heating_bp.route('/<building>', methods=['GET', 'POST'])
@login_required
def heating(building):
    project = get_project()
    buildings = dbo.get_all_project_buildings(project.id)
        
    if request.method == "GET":
        if building is None:
            return render_template('heating.html',
                                user=current_user,
                                project=project,
                                heating=None,
                                project_buildings=buildings,
                                building=None)
        else:
            building = dbo.get_building(building)
            heatprops = dboh.get_building_heating_settings(building.id)
            rooms = building.rooms
            return render_template('heating.html',
                    user=current_user,
                    project=project,
                    heating=heatprops,
                    project_buildings=buildings,
                    building = building,
                    rooms = rooms)
        
    if request.method == "POST":
        requested_building_id = escape(request.form.get("project_building"))
        return redirect(url_for("heating.heating", building=requested_building_id))
    
@heating_bp.route('/update_building_settings', methods=['POST'])
@login_required
def update_building_settings():
    return redirect(url_for('heating.heating'))
