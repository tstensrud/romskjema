from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, session, request
from flask_login import login_required, current_user
from .. import db_operations as dbo
from .. import db_ops_heating as dboh
from ..globals import get_project, pattern_float, pattern_int, replace_and_convert_to_float
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
            heat_loss_project = []
            heat_loss_project.append(dboh.sum_heat_loss_project(project.id))
            heat_loss_project.append(dboh.sum_heat_loss_project_chosen(project.id))
            return render_template('heating.html',
                                user=current_user,
                                project=project,
                                heating=None,
                                project_buildings=buildings,
                                building=None,
                                summary=heat_loss_project)
        else:
            building = dbo.get_building(building)
            heatloss_sum = []
            heatloss_sum.append(dboh.sum_heat_loss_building(building.id))
            heatloss_sum.append(dboh.sum_heat_loss_chosen_building(building.id))
            heatprops = dboh.get_building_heating_settings(building.id)
            rooms = building.rooms
            return render_template('heating.html',
                    user=current_user,
                    project=project,
                    heating=heatprops,
                    project_buildings=buildings,
                    building=building,
                    rooms = rooms,
                    heatloss=heatloss_sum)
        
    if request.method == "POST":
        requested_building_id = escape(request.form.get("project_building"))
        return redirect(url_for("heating.heating", building=requested_building_id))
    
@heating_bp.route('/building_heating_settings', methods=['POST'])
@login_required
def building_heating_settings():
    if request.is_json:
        data = request.get_json()
        building_id = escape(data["building_id"])
        processed_data = {}

        # Replace ,-s to .-s and convert values to float
        for key, value in data.items():
            if key == "building_id":
                processed_data[key] = value
            else:
                processed_data[key] = replace_and_convert_to_float(escape(value))
        
        if dboh.update_building_heating_settings(processed_data):
            rooms_in_building = dboh.get_all_rooms_heating_building(building_id)
            for room in rooms_in_building:
                dboh.calculate_total_heat_loss_for_room(room.id)
            flash(f"Oppdatert innstillinger for bygg {building_id}", category="success")
            response = {"success": True, "redirect": url_for("heating.heating", building=building_id)}
        else:
            flash("Kunne ikke oppdatere bygningsdata")
            response = {"success": False, "redirect": url_for("heating.heating", building=building_id)}
            return jsonify(response)
    return jsonify(response)

@heating_bp.route('/update_room_info', methods=['GET', 'POST'])
@login_required
def update_room_info():
    if request.is_json:
        data = request.get_json()
        building_id = escape(data["building_id"])
        processed_data = {}
        for key, value in data.items():
            if key == "heat_source" or key == "comment":
                processed_data[key] = escape(value)
            else:
                value_cleaned_up = escape(value.replace(",", "."))
                processed_data[key] = pattern_float(value_cleaned_up)
        if dboh.update_room_heating_data(escape(data["vent_data_id"]), processed_data):
            if dboh.calculate_total_heat_loss_for_room(data["vent_data_id"]):
                flash("Data oppdatert", category="success")
                response = {"success": True, "redirect": url_for("heating.heating", building=building_id)}
            else:
                flash("Kunne ikke beregne varmetap", category="error")
                response = {"success": False, "redirect": url_for("heating.heating", building=building_id)}
                return jsonify(response)
        else:
            flash("kunne ikke oppdatere varmedaga", category="error")
            response = {"success": False, "redirect": url_for("heating.heating", building=building_id)}
    return jsonify(response)
