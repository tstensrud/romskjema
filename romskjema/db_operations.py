from sqlalchemy import func, and_
from . import models, db
from flask_login import login_required
import math

@login_required
def get_all_project_names():
    project_names = []
    projects = models.Projects.query.all()
    for project_name in projects:
        project_names.append(project_name.ProjectName)
    return project_names

@login_required
def get_building_id(project_id: int, building_name: str) -> int:
    building = db.session.query(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.BuildingName == building_name)).first()
    return building.id


'''
Room list methods
'''
@login_required
def get_room_id(project_id: int, building_id: int, room_number: str) -> int:
    room = db.session.query(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id, models.Rooms.RoomNumber == room_number)).first()
    return room.id

@login_required
def delete_room(project_id: int, building_id: int, room_id: int) -> bool:
    vent_properties = db.session.query(models.VentilationProperties).filter(models.VentilationProperties.RoomId == room_id).first()
    if vent_properties:
        db.session.delete(vent_properties)
        db.session.commit()
    
    room = db.session.query(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id, models.Rooms.id == room_id)).first()
    if room:
        db.session.delete(room)
        db.session.commit()
        return True
    else:
        return False

'''
Ventilation methods
'''
@login_required
def get_specifications():
    spec_list = []
    specifications = models.Specifications.query.all()
    for spec in specifications:
        spec_list.append(spec)
    return spec_list

@login_required
def initial_ventilation_calculations(project_id: int, building_id: int, room_id: int) -> None:
    vent_properties_room = db.session.query(models.VentilationProperties).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id, models.Rooms.id == room_id)).first()
    room = vent_properties_room.rooms
    vent_properties_room.AirPersonSum = round((room.RoomPopulation * vent_properties_room.AirPerPerson),1)
    vent_properties_room.AirEmissionSum = round((room.Area * vent_properties_room.AirEmission), 1)
    vent_properties_room.AirDemand = round((vent_properties_room.AirPersonSum + vent_properties_room.AirEmissionSum + vent_properties_room.AirProcess),1)
    vent_properties_room.AirSupply = round((math.ceil(vent_properties_room.AirDemand / 10) * 10), 1)
    vent_properties_room.AirExtract = vent_properties_room.AirSupply
    vent_properties_room.AirChosen = round((vent_properties_room.AirSupply / room.Area), 1)
    db.session.commit()

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
    supply = db.session.query(func.sum(models.VentilationProperties.AirSupply)).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).scalar()
    return supply

@login_required
def summarize_extract_air_building(project_id: int, building_id: int) -> float:
    supply = db.session.query(func.sum(models.VentilationProperties.AirExtract)).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).scalar()
    return supply

@login_required
def get_room_type_data(room_type_id: int, specification: str):
    room_data_object = db.session.query(models.RoomTypes).join(models.Specifications).filter(and_(models.Specifications.name == specification, models.RoomTypes.id == room_type_id)).first()
    return room_data_object

@login_required
def get_specification_room_types(specification: str):
    room_types = db.session.query(models.RoomTypes).join(models.Specifications).filter(models.Specifications.name == specification).all()
    return room_types

@login_required
def get_specification_room_data(specification_name: str):
    data = db.session.query(models.RoomTypes).join(models.Specifications).filter(models.Specifications.name == specification_name).all()
    return data