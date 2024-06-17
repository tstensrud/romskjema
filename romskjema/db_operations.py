from sqlalchemy import func, and_
from . import models, db
from . import db_ops_energy as dboh
from flask_login import login_required
import math
from . import globals

'''
Project methods
'''
@login_required
def get_all_projects():
    projects = models.Projects.query.all()
    return projects

@login_required
def get_project(project_id: int) -> models.Projects:
    project = db.session.query(models.Projects).filter(models.Projects.id == project_id).first()
    return project

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
def get_building(building_id: int) -> models.Buildings:
    building = db.session.query(models.Buildings).filter(models.Buildings.id == building_id).first()
    return building

@login_required
def new_building(project_id: int, building_name: str) -> bool:
    new_building = models.Buildings(ProjectId = project_id, BuildingName = building_name)
    try:
        db.session.add(new_building)
        db.session.commit()
        dboh.set_up_energy_settings_building(project_id, new_building.id)
        return True
    except Exception as e:
        globals.log(f"new building: {e}")
        db.session.rollback()
        return False
    
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
def new_room(building_id: int, room_type_id: int, floor: str, room_number: str, room_name: str, area: float, room_pop: int):
    new_room = models.Rooms(BuildingId = building_id, RoomTypeId = room_type_id, Floor = floor, RoomNumber = room_number,
                                RoomName = room_name, Area = area, RoomPopulation = room_pop)
    try:
        db.session.add(new_room)
        db.session.commit()
        return new_room.id
    except Exception as e:
        globals.log(e)
        db.session.rollback()
        return False
    
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
        except Exception as e:
            db.session.rollback()
            globals.log(f"delete_room() first try/except block: {e}")
            return False
    
    energy_properties = db.session.query(models.RoomEnergyProperties).filter(models.RoomEnergyProperties.RoomId == room_id).first()
    if energy_properties:
        try:
            db.session.delete(energy_properties)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            globals.log(f"Feil sletting av rom heating properties {e}")
            return False
    
    room = db.session.query(models.Rooms).filter(models.Rooms.id == room_id).first()
    if room:
        try:
            db.session.delete(room)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            globals.log(f"delete_room() second try/except block: {e}")
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
        globals.log(f"update_room_data(): {e}")
        return False

'''
Ventilation methods
'''
@login_required
def new_vent_prop_room(room_id: int, air_per_person: float, air_emission: float, air_process: float,
                       air_minimum: float, ventilation_principle: str, heat_exchange: str, room_control: str,
                       notes: str, db_technical: str, db_neighbour: str, db_corridor: str, comments: str) -> bool:
    room_ventilation_properties = models.RoomVentilationProperties(RoomId = room_id,
                                                                        AirPerPerson=air_per_person,
                                                                        AirEmission=air_emission,
                                                                        AirProcess=air_process,
                                                                        AirMinimum=air_minimum,
                                                                        AirSupply = 0.0,
                                                                        AirExtract= 0.0,
                                                                        VentilationPrinciple=ventilation_principle,
                                                                        HeatExchange=heat_exchange,
                                                                        RoomControl=room_control,
                                                                        Notes=notes,
                                                                        DbTechnical=db_technical,
                                                                        DbNeighbour=db_neighbour,
                                                                        DbCorridor=db_corridor,
                                                                        Comments=comments)
    try:
        db.session.add(room_ventilation_properties)
        db.session.commit()
        return True
    except Exception as e:
        globals.log(f"new vent prop room: {e}")
        db.session.rollback()
        return False
    
@login_required
def get_room_vent_prop(vent_prop_id: int) -> models.RoomVentilationProperties:
    vent_prop = db.session.query(models.RoomVentilationProperties).filter(models.RoomVentilationProperties.id == vent_prop_id).first()
    return vent_prop

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
    except Exception as e:
        globals.log(f"initial_ventilation_calculations: {e}")
        db.session.rollback()
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
    except Exception as e:
        globals.log(f"update_ventilation_calculations: {e}")
        db.session.rollback()
        return False

@login_required
def update_ventilation_table(vent_prop_id: int, new_supply: float, new_extract: float, system=None, comment=None) -> bool:
    print(f"System id for update ventilation table: {system}")
    vent_properties_room = get_room_vent_prop(vent_prop_id)
    room = vent_properties_room.room_ventilation
    vent_properties_room.AirSupply = new_supply
    vent_properties_room.AirExtract = new_extract
    vent_properties_room.AirChosen = round((new_supply / room.Area), 1)
    if system is not None:
        vent_properties_room.System = system
    if comment is not None:
        vent_properties_room.Comments = comment
    try:
        db.session.commit()
        if system is not None:
            update_system_airflows(vent_properties_room.SystemId)
            dboh.calculate_total_heat_loss_for_room(room.energy_properties.id)
        return True
    except Exception as e:
        db.session.rollback()
        globals.log(f"update_ventilation_table: {e}")
        return False
    

@login_required
def set_system_for_room_vent_prop(room_vent_prop_id: int, system_id: int) -> bool:
    vent_prop = get_room_vent_prop(room_vent_prop_id)
    vent_prop.SystemId = system_id

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        globals.log(f"set_system_for_room_vent_prop: {e}")
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
def get_summary_of_ventilation_system(project_id: int, system_name: str) -> float:
    supply = db.session.query(func.sum(models.RoomVentilationProperties.AirExtract)).join(models.Rooms).join(models.Buildings).join(models.Projects).filter(and_(models.Projects.id == project_id, models.RoomVentilationProperties.System == system_name)).scalar()
    return supply

'''
Ventilation systems
'''
@login_required
def new_ventilation_system(project_id: int, system_number: str, placement: str, service_area: str, heat_ex: str, airflow: float, special: str) -> bool:
    system = models.VentilationSystems(ProjectId=project_id, 
                                       SystemName=system_number, 
                                       Location=placement, 
                                       ServiceArea=service_area, 
                                       HeatExchange=heat_ex, 
                                       AirFlow=airflow, 
                                       AirFlowSupply=0.0, 
                                       AirFlowExtract=0.0,
                                       SpecialSystem=special)
    try:
        db.session.add(system)
        db.session.commit()
        return True
    except Exception as e:
        globals.log(f"new_ventilation_system: {e}")
        db.session.rollback()
        return False

@login_required
def delete_system(system_id: int) -> bool:
    rooms = db.session.query(models.RoomVentilationProperties).join(models.VentilationSystems).filter(models.VentilationSystems.id==system_id).all()
    db.session.query(models.VentilationSystems).filter(models.VentilationSystems.id == system_id).delete()
    
    print(rooms)
    for room in rooms:
        room.SystemId = None
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        globals.log(f"delete system: {e}")
        return False
    
@login_required
def get_all_systems(project_id: int) -> list:
    systems = db.session.query(models.VentilationSystems).join(models.Projects).filter(models.Projects.id == project_id).all()
    return systems

@login_required
def get_system(system_id: int) -> models.VentilationSystems:
    system = db.session.query(models.VentilationSystems).filter(models.VentilationSystems.id == system_id).first()
    return system

@login_required
def check_if_system_number_exists(project_id: int, system_number: str) -> bool:
    system = db.session.query(models.VentilationSystems).join(models.Projects).filter(models.Projects.id == project_id, models.VentilationSystems.SystemName == system_number).first()
    if system:
        return True
    else:
        return False
    
@login_required
def get_system_names(project_id: int) -> list:
    system_names = db.session.query(models.VentilationSystems.SystemName).join(models.Projects).filter(models.Projects.id == project_id).all()
    return [system_name[0] for system_name in system_names]

@login_required
def summarize_system_supply(system_id) -> float:
    supply = db.session.query(func.sum(models.RoomVentilationProperties.AirSupply)).join(models.VentilationSystems).filter(models.VentilationSystems.id == system_id).scalar()
    return supply

@login_required
def summarize_system_extract(system_id) -> float:
    extract = db.session.query(func.sum(models.RoomVentilationProperties.AirExtract)).join(models.VentilationSystems).filter(models.VentilationSystems.id == system_id).scalar()
    return extract

@login_required
def update_system_airflows(system_id: int) -> bool:
    system = get_system(system_id)
    if system:
        system.AirFlowSupply = summarize_system_supply(system_id)
        system.AirFlowExtract = summarize_system_extract(system_id)
    else:
        print("no system found")
    try:
        db.session.commit()
        return True
    except Exception as e:
        globals.log(f"update_system_air_flows: {e}")
        db.session.rollback()
        return False

@login_required
def update_airflow_changed_system(system_id_new: int, system_id_old: int) -> bool:
    new_system = get_system(system_id_new)
    old_system = get_system(system_id_old)
    new_system.AirFlowSupply = summarize_system_supply(system_id_new)
    new_system.AirFlowExtract = summarize_system_extract(system_id_new)
    old_system.AirFlowSupply = summarize_system_supply(system_id_old)
    old_system.AirFlowExtract = summarize_system_extract(system_id_old)

    try:
        db.session.commit()
        return True
    except Exception as e:
        globals.log(f"update_airflow_changed_system: {e}")
        db.session.rollback()
        return False

@login_required
def update_system_info(system_id: int, system_number: str, system_location: str, service_area: str, airflow: float, heat_ex: str) -> bool:
    system = get_system(system_id)
    system.SystemName = system_number
    system.Location = system_location
    system.ServiceArea = service_area
    system.AirFlow = airflow
    system.HeatExchange = heat_ex
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        globals.log(f"update_system_info: {e}")
        return False


'''
Specifications
'''
@login_required
def new_specifitaion(name: str) -> bool:
    specification = models.Specifications(name=name)
    try:
        db.session.add(specification)
        db.session.commit()
        return True
    except Exception as e:
        globals.log(f"new specification: {e}")
        db.session.rollback()
        return False

@login_required
def get_specification_by_name(name: str) -> models.Specifications:
    spec = db.session.query(models.Specifications).filter(models.Specifications.name == name).first()
    return spec

# Get list of all specifications in database
@login_required
def get_specifications() -> list:
    spec_list = []
    specifications = models.Specifications.query.all()
    for spec in specifications:
        spec_list.append(spec)
    return spec_list

@login_required
def find_specification_name(name: str) -> bool:
    name = db.session.query(models.Specifications.name).filter(models.Specifications.name == name).first()
    if name:
        return True
    else:
        return False
    
# Get data for a specific roomtype in a specification
@login_required
def get_room_type_data(room_type_id: int, specification: str):
    room_data_object = db.session.query(models.RoomTypes).join(models.Specifications).filter(and_(models.Specifications.name == specification, models.RoomTypes.id == room_type_id)).first()
    return room_data_object

@login_required
def get_room_type_name(specification: str, room_id: int) -> str:
    room_type_name = db.session.query(models.RoomTypes.name).join(models.Specifications).filter(models.Specifications.name == specification, models.RoomTypes.id == room_id).first()
    return room_type_name

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

@login_required
def new_specification_room_type(specification_id: int, name: str, air_per_person: float, air_emission: float, air_process: float,
                 air_minimum: float, vent_principle: str, heat_ex: str, room_control: str, notes: str,
                 dbt: str, dbn: str, dbc: str, comments: str) -> bool:
    room = models.RoomTypes(specification_id=specification_id,
                            name=name,
                            air_per_person=air_per_person,
                            air_emission=air_emission,
                            air_process=air_process,
                            air_minimum=air_minimum,
                            ventilation_principle=vent_principle,
                            heat_exchange=heat_ex,
                            room_control=room_control,
                            notes=notes,
                            db_technical=dbt,
                            db_neighbour=dbn,
                            db_corridor=dbc,
                            comments=comments)
    try:
        db.session.add(room)
        db.session.commit()
        return True
    except Exception as e:
        globals.log(f"create new room type {e}")
        db.session.rollback()
        return False