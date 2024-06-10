from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import login_required, current_user
from .. import db_operations as dbo

specifications_bp = Blueprint('specifications',__name__, static_folder='static', template_folder='templates')

@specifications_bp.route('/', defaults={'specification': None}, methods=['GET', 'POST'])
@specifications_bp.route('/<specification>', methods=['GET', 'POST'])
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