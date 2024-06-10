
from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, request
from flask_login import login_required, current_user
from .. import db_operations as dbo
from ..globals import get_project, pattern_int, pattern_float

ventsystems_bp = Blueprint('ventsystems', __name__, static_folder='static', template_folder='templates')

@login_required
@ventsystems_bp.route('/', methods=['GET', 'POST'])
def ventsystems():
    project = get_project()
    
    if request.method == "POST":
        system_number = request.form.get("system_number").strip()
        if dbo.check_if_system_number_exists(project.id, system_number):
            flash("Systemnummer finnes allerede", category="error")
            return redirect(url_for('ventsystems.ventsystems'))
        
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
            return redirect(url_for('ventsystems.ventsystems'))
        else:
            flash("Kunne ikke opprette system.", category="error")
            return redirect(url_for('ventsystems.ventsystems'))
    
    if request.method == "GET":
        systems = dbo.get_all_systems(project.id)
        return render_template("vent_systems.html", 
                                user=current_user, 
                                project=project,
                                systems=systems)


@login_required
@ventsystems_bp.route('/update_system', methods=['POST'])
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
        response = {"success": True, "redirect": url_for("ventsystems.ventsystems")}
    else:
        flash("Kunne ikke oppdatere system-data", category="error")
        response = {"success": False, "redirect": url_for("ventsystems.ventsystems")}
    
    return jsonify(response)

@login_required
@ventsystems_bp.route('/delete_system', methods=['POST'])
def delete_system():
    if request.method == "POST":
        data = request.get_json()
        system_id = data["system_id"]
        if dbo.delete_system(system_id):
            flash("System slettet", category="success")
            response = {"success": True, "redirect": url_for("ventsystems.ventsystems")}
        else:
            flash("Kunne ikke slette system", category="error")
            response = {"success": False, "redirect": url_for("ventsystems.ventsystems")}
        return jsonify(response)