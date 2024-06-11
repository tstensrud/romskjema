from flask import Blueprint, redirect, url_for, render_template, flash, jsonify, session, request
from flask_login import login_required, current_user
from .. import models, db
from .. import db_operations as dbo
from .. import db_ops_heating as dboh
from ..globals import get_project, pattern_float, pattern_int
from markupsafe import escape

heating_bp = Blueprint('heating', __name__, static_folder="static", template_folder="templates")


@heating_bp.route('/', methods=["GET"])
@login_required
def heating():
    project = get_project()
    heatprops = dboh.get_building_heating_settings(1)

    return render_template('heating.html',
                           user=current_user,
                           project=project,
                           heating=heatprops)

@heating_bp.route('/update_building_settings', methods=['POST'])
@login_required
def update_building_settings():
    return redirect(url_for('heating.heating'))
