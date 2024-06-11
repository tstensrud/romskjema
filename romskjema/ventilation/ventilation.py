from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, request, session
from flask_login import login_required, current_user
from .. import db_operations as dbo
from ..globals import get_project, pattern_float
from markupsafe import escape

ventilation_bp = Blueprint('ventilation', __name__, static_folder='static', template_folder='templates')

@ventilation_bp.route('/', defaults={'building_id': None}, methods=['GET', 'POST'])
@ventilation_bp.route('/<building_id>', methods=['GET', 'POST'])
@login_required
def ventilation(building_id):
    project = get_project()

    if request.method == "POST":       
        # Showing specific buildings in the table
        requested_building_id = escape(request.form.get("project_building"))
        if requested_building_id != "none" and requested_building_id != "showall":
            return redirect(url_for("ventilation.ventilation", building_id = requested_building_id))
        else:
            return redirect(url_for("ventilation.ventilation", building_id = "showall"))
    
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

@ventilation_bp.route('/update_ventilation', methods=['POST'])
@login_required
def update_ventilation():    
    data = request.get_json()

    # If system is updated
    if data["system_update"] == True:
        old_system_id = escape(data["old_system_id"])
        system_id = escape(data["system_id"])
        vent_prop_id = escape(data["row_id"])
        
        if old_system_id == "none":
            if dbo.set_system_for_room_vent_prop(vent_prop_id, system_id):
                dbo.update_system_airflows(system_id)
                flash("System satt", category="success")
                response = {"success": True, "redirect": url_for("ventilation.ventilation")}
            else:
                flash("System kunne ikke settes", category="error")
                response = {"success": False, "redirect": url_for("ventilation.ventilation")}
            return jsonify(response)

        if old_system_id == system_id:
            if dbo.update_system_airflows(system_id):
                flash("System oppdatert", category="success")
                response = {"success": True, "redirect": url_for("ventilation.ventilation")}
            else:
                flash("Kunne ikke oppdatere luftmengde dbo.update_system_airflows", category="error")
                response = {"success": False, "redirect": url_for("ventilation.ventilation")}
        else:
            dbo.set_system_for_room_vent_prop(vent_prop_id, system_id)
            if dbo.update_airflow_changed_system(system_id, old_system_id):
                flash("System oppdatert", category="success")
                response = {"success": True, "redirect": url_for("ventilation.ventilation")}
            else:
                flash("Kunne ikke oppdatere luftmengder: update_airflow_changed_system", category="error")
                response = {"success": False, "redirect": url_for("ventilation.ventilation")}
        return jsonify(response)




    
    vent_prop_id = escape(data["vent_data_id"])
    supply = escape(data["supply_air"].strip())
    
    new_supply = pattern_float(supply)
    if new_supply is False:
        flash("Tilluft kan kun inneholde tall.", category="error")
        response = {"success": False, "redirect": url_for("ventilation.ventilation")}
    extract = escape(data["extract_air"].strip())
    
    new_extract = pattern_float(extract)
    if new_extract is False:
        flash("Avtrekk kan kun inneholde tall.", category="error")
        response = {"success": False, "redirect": url_for("ventilation.ventilation")}
    
    comment = escape(data["comment"].strip())

    if dbo.update_ventilation_table(vent_prop_id, new_supply, new_extract, None, comment):
        flash('Data oppdatert', category="success")
        response = {"success": True, "redirect": url_for("ventilation.ventilation")}
    else:
        flash("Kunne ikke oppdatere verdier.", category="error")
        response = {"success": False, "redirect": url_for("ventilation.ventilation")}
    return jsonify(response)
