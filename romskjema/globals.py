from flask import session
from flask_login import login_required
from . import models
import re

def pattern_float(input) -> float:
    pattern = r"\d+(\.\d+)?"
    match = re.search(pattern, input)
    if match:
        return float(match.group())

def pattern_int(input) -> int:
    pattern = r"\d+"
    output = re.findall(pattern, input)
    return int(''.join(output))

@login_required
def get_project():
    project_id = session.get('project_id')
    project = models.Projects.query.get(project_id)
    return project