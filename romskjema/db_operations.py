from sqlalchemy import func, and_
from . import models, db
from flask_login import login_required
import math


'''
Project methods
'''
@login_required
def get_all_projects():
    projects = models.Projects.query.all()
    return projects

@login_required
def get_all_project_names():
    project_names = []
    projects = models.Projects.query.all()
    for project_name in projects:
        project_names.append(project_name.ProjectName)
    return project_names

@login_required
def get_all_project_rooms(project_id):
    rooms = db.session.query(models.Rooms).join(models.Buildings).join(models.Projects).filter(models.Projects.id == project_id).order_by(models.Buildings.BuildingName, models.Rooms.Floor).all()
    return rooms

@login_required
def get_all_project_buildings(project_id: int):
    #buildings = db.session.query(models.Buildings).filter(models.Buildings.ProjectId == project_id).all()
    buildings = db.session.query(models.Buildings).join(models.Projects).filter(models.Projects.id == project_id).all()
    return buildings

@login_required
def check_for_existing_project_number(project_number: str) -> bool:
    project = models.Projects.query.filter_by(ProjectNumber = project_number).first()
    if project:
        return True
    else:
        return False


'''
Building methods
'''
@login_required
def get_all_project_buildings(project_id: int):
    buildings = models.Buildings.query.filter_by(ProjectId = project_id).all()
    return buildings
@login_required
def get_building_id(project_id: int, building_name: str) -> int:
    building = db.session.query(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.BuildingName == building_name)).first()
    return building.id

'''
Rooms methods
'''

@login_required
def get_room(room_id: int) -> models.Rooms:
    room = db.session.query(models.Rooms).filter(models.Rooms.id == room_id).first()
    return room

@login_required
def get_room_id(project_id: int, building_id: int, room_number: str) -> int:
    room = db.session.query(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id, models.Rooms.RoomNumber == room_number)).first()
    return room.id

@login_required
def delete_room(room_id: int) -> bool:
    vent_properties = db.session.query(models.RoomVentilationProperties).filter(models.RoomVentilationProperties.RoomId == room_id).first()
    if vent_properties:
        try:
            db.session.delete(vent_properties)
            db.session.commit()
        except Exception:
            return False
    
    room = db.session.query(models.Rooms).filter(models.Rooms.id == room_id).first()
    if room:
        try:
            db.session.delete(room)
            db.session.commit()
            return True
        except Exception:
            return False
    else:
        return False

@login_required
def check_if_roomnumber_exists(project_id, building_id, room_number) -> bool:
    room = db.session.query(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id, models.Rooms.RoomNumber == room_number)).first()
    if room:
        return True
    else:
        return False

@login_required
def update_room_data(room_id: int, new_room_number: str, new_room_name: str, new_area: float, new_pop: int, new_comment: str) -> bool:
    room = get_room(room_id)
    room.Area = new_area
    room.RoomPopulation = new_pop
    room.RoomNumber = new_room_number
    room.RoomName = new_room_name
    room.Comments = new_comment
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(e)
        return False

'''
Ventilation methods
'''
# Get list of all specifications in database
@login_required
def get_specifications() -> list:
    spec_list = []
    specifications = models.Specifications.query.all()
    for spec in specifications:
        spec_list.append(spec)
    return spec_list

@login_required
def initial_ventilation_calculations(room_id: int) -> bool:
    vent_properties_room = db.session.query(models.RoomVentilationProperties).filter(models.RoomVentilationProperties.RoomId == room_id).first()
    room = get_room(room_id)
    print(room.RoomPopulation)
    vent_properties_room.AirPersonSum = round((room.RoomPopulation * vent_properties_room.AirPerPerson),1)
    vent_properties_room.AirEmissionSum = round((room.Area * vent_properties_room.AirEmission), 1)
    vent_properties_room.AirDemand = round((vent_properties_room.AirPersonSum + vent_properties_room.AirEmissionSum + vent_properties_room.AirProcess),1)
    vent_properties_room.AirSupply = round((math.ceil(vent_properties_room.AirDemand / 10) * 10), 1)
    vent_properties_room.AirExtract = vent_properties_room.AirSupply
    vent_properties_room.AirChosen = round((vent_properties_room.AirSupply / room.Area), 1)
    try:
        db.session.commit()
        return True
    except Exception:
        return False

@login_required
def update_ventilation_calculations(room_id: int) -> bool:
    vent_properties_room = db.session.query(models.RoomVentilationProperties).filter(models.RoomVentilationProperties.RoomId == room_id).first()
    room = get_room(room_id)
    vent_properties_room.AirPersonSum = round((room.RoomPopulation * vent_properties_room.AirPerPerson),1)
    vent_properties_room.AirEmissionSum = round((room.Area * vent_properties_room.AirEmission), 1)
    vent_properties_room.AirDemand = round((vent_properties_room.AirPersonSum + vent_properties_room.AirEmissionSum + vent_properties_room.AirProcess),1)
    vent_properties_room.AirChosen = round((vent_properties_room.AirSupply / room.Area), 1)
    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

@login_required
def update_supply_extract(vent_prop_id: int, new_supply: float, new_extract: float, system=None, comment=None) -> bool:
    vent_properties_room = db.session.query(models.RoomVentilationProperties).filter(models.RoomVentilationProperties.id == vent_prop_id).first()
    room = vent_properties_room.rooms
    vent_properties_room.AirSupply = new_supply
    vent_properties_room.AirExtract = new_extract
    vent_properties_room.AirChosen = round((new_supply / room.Area), 1)
    if system is not None:
        vent_properties_room.System = system
    if comment is not None:
        vent_properties_room.Comments = comment
    try:
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

@login_required
def summarize_building_area(project_id: int, building_id: int) -> float:
    total_building_area = db.session.query(func.sum(models.Rooms.Area)).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).scalar()
    return total_building_area

@login_required
def summarize_project_area(project_id: int) -> float:
    area = db.session.query(func.sum(models.Rooms.Area)).join(models.Buildings).join(models.Projects).filter(models.Projects.id == project_id).scalar()
    return area

@login_required
def summarize_supply_air_building(project_id: int, building_id: int) -> float:
    supply = db.session.query(func.sum(models.RoomVentilationProperties.AirSupply)).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).scalar()
    return supply

@login_required
def summarize_extract_air_building(project_id: int, building_id: int) -> float:
    supply = db.session.query(func.sum(models.RoomVentilationProperties.AirExtract)).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).scalar()
    return supply

@login_required
def get_ventilation_data_rooms_in_building(project_id: int, building_id: int):
    data = db.session.query(models.RoomVentilationProperties).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).order_by(models.Rooms.Floor).all()
    return data

@login_required
def get_ventlation_data_all_rooms_project(project_id: int):
    data = db.session.query(models.RoomVentilationProperties).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(models.Projects.id == project_id).order_by(models.Buildings.BuildingName, models.Rooms.Floor).all()
    return data

@login_required
def get_all_system_names(project_id: int) -> list:
    system_names = db.session.query(models.RoomVentilationProperties.System).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(models.Projects.id == project_id).distinct().all()
    return [system[0] for system in system_names]

@login_required
def get_summary_of_ventilation_system(project_id: int, system_name: str) -> float:
    supply = db.session.query(func.sum(models.RoomVentilationProperties.AirExtract)).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.RoomVentilationProperties.System == system_name)).scalar()
    return supply
'''
Systems
'''
@login_required
def create_system(project_id: int, system_name: str, airflow: float) -> bool:
    system = models.VentilationSystems(project_id, system_name, airflow, 0.0, 0.0)
    try:
        db.session.add(system)
        db.session.commit()
        return True
    except Exception:
        return False
    
'''
Specifications
'''
# Get data for a specific roomtype in a specification
@login_required
def get_room_type_data(room_type_id: int, specification: str):
    room_data_object = db.session.query(models.RoomTypes).join(models.Specifications).filter(and_(models.Specifications.name == specification, models.RoomTypes.id == room_type_id)).first()
    return room_data_object

# Get name of all room types for a specific specification
@login_required
def get_specification_room_types(specification: str):
    room_types = db.session.query(models.RoomTypes).join(models.Specifications).filter(models.Specifications.name == specification).all()
    return room_types

# Get all room types and data for a specific specification
@login_required
def get_specification_room_data(specification_name: str):
    data = db.session.query(models.RoomTypes).join(models.Specifications).filter(models.Specifications.name == specification_name).all()
    return data