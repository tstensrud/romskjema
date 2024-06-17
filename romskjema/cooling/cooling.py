from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, session, request
from flask_login import login_required, current_user
from .. import db_operations as dbo
from .. import db_ops_energy as dboh
from ..globals import pattern_float, pattern_int, replace_and_convert_to_float
from markupsafe import escape

cooling_bp = Blueprint('cooling', __name__, static_folder='static', template_folder='templates')

@cooling_bp.route('/', defaults={'building': None}, methods=['GET', 'POST'])
@cooling_bp.route('/<building>', methods=['GET', 'POST'])
@login_required
def cooling(project_id, building):
    project = dbo.get_project(project_id)
    project_buildings = dbo.get_all_project_buildings(project_id)
    endpoint = request.endpoint
    cooling = None
    if request.method == "GET":
        if building is None:
            return render_template('cooling.html',
                                user=current_user,
                                project_id = project_id,
                                project=project,
                                project_buildings=project_buildings,
                                endpoint=endpoint,
                                cooling=cooling,
                                building=building)
        else:
            building = dbo.get_building(building)
            coolingprops = dboh.get_building_energy_settings(building.id)
            rooms = building.rooms
            return render_template('cooling.html',
                                   user=current_user,
                                   project=project,
                                   cooling=coolingprops,
                                   building=building,
                                   project_buildings=project_buildings,
                                   rooms=rooms,
                                   project_id = project_id,
                                   endpoint=endpoint)
    elif request.method == "POST":
        requested_building_id = escape(request.form.get("project_building"))
        return redirect(url_for('cooling.cooling', building=requested_building_id, project_id=project_id))

@login_required
@cooling_bp.route('/building_cooling_settings', methods=['POST'])
def building_cooling_settings(project_id):
    if request.is_json():
        data = request.get_json()
        building_id = escape(data["building_id"])
        processed_data = {}
        
        for key, value in data.items():
            if key == "building_id":
                processed_data[key] = value
            else:
                processed_data[key] = replace_and_convert_to_float(escape(value))
        
