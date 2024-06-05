from sqlalchemy import func, and_
from . import models, db
from flask_login import login_required
import math

@login_required
def initial_ventilation_calculations(project_id: int, building_id: int, room_id: int) -> None:
    vent_properties_room = db.session.query(models.VentilationProperties).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id, models.Rooms.id == room_id)).first()
    room = vent_properties_room.rooms
    vent_properties_room.AirPersonSum = room.RoomPopulation * vent_properties_room.AirPerPerson
    vent_properties_room.AirEmissionSum = room.Area * vent_properties_room.AirEmission
    vent_properties_room.AirDemand = vent_properties_room.AirPersonSum + vent_properties_room.AirEmissionSum + vent_properties_room.AirProcess
    vent_properties_room.AirSupply = math.ceil(vent_properties_room.AirDemand / 10) * 10
    vent_properties_room.AirExtract = vent_properties_room.AirSupply
    vent_properties_room.AirChosen = vent_properties_room.AirSupply / room.Area
    db.session.commit()

def summarize_building_area(project_id: int, building_id: int) -> float:
    total_building_area = db.session.query(func.sum(models.Rooms.Area)).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).scalar()
    return total_building_area

def summarize_project_area(project_id: int) -> float:
    area = db.session.query(func.sum(models.Rooms.Area)).join(models.Buildings).join(models.Projects).filter(models.Projects.id == project_id).scalar()
    return area

def summarize_supply_air_building(project_id: int, building_id: int) -> float:
    supply = db.session.query(func.sum(models.VentilationProperties.AirSupply)).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).scalar()
    return supply

def summarize_extract_air_building(project_id: int, building_id: int) -> float:
    supply = db.session.query(func.sum(models.VentilationProperties.AirExtract)).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.Buildings.id == building_id)).scalar()
    return supply
