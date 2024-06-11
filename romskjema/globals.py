from flask import session
from flask_login import login_required
from . import models
import re

def pattern_float(input):
    pattern = r"\d+(\.\d+)?"
    match = re.search(pattern, input)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return False

def pattern_int(input):
    pattern = r"\d+"
    output = re.findall(pattern, input)
    try:
        return int(''.join(output))
    except ValueError:
        return False

def replace_and_convert_to_float(input: str):
    replaced = input.replace(",", ".")
    try:
        float_value = float(replaced)
        return float_value
    except ValueError:
        return False
    
@login_required
def get_project():
    project_id = session.get('project_id')
    project = models.Projects.query.get(project_id)
    return project

def log(entry):
    with open(f"log.txt", "a") as file:
        file.writelines(f"{entry}\n")