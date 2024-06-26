from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    logged_in = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    todo_item = db.relationship('TodoItem', backref='user', uselist=False, lazy=True)


'''
# TODO-items
'''
class TodoItem(db.Model):
    __tablename__ = "TodoItem"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    content = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_completed = db.Column(db.String(10))
    completed_by = db.Column(db.String(100))

class Projects(db.Model):
    __tablename__ = "Projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectNumber = db.Column(db.Integer, nullable=False)
    ProjectName = db.Column(db.String(50), nullable=False)
    ProjectDescription = db.Column(db.Text)
    Specification = db.Column(db.String(50))

    todo_item = db.relationship('TodoItem', backref='project', uselist=False, lazy=True)
    buildings = db.relationship('Buildings', backref='project_buildings', uselist=False, lazy=True)
    ventilation_systems = db.relationship('VentilationSystems', backref='project_ventilation_systems', uselist=False, lazy=True)
    


class Buildings(db.Model):
    __tablename__ = "Buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    BuildingName = db.Column(db.String(100), nullable=False)

    rooms = db.relationship('Rooms', backref='building', lazy=True)
    energy_properties = db.relationship('BuildingEnergySettings', backref='heating', uselist=False, lazy=True)
    


class Rooms(db.Model):
    __tablename__ = "Rooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BuildingId = db.Column(db.Integer, db.ForeignKey('Buildings.id'), nullable=False)
    RoomTypeId = db.Column(db.Integer, db.ForeignKey('RoomTypes.id'), nullable=False)
    Floor = db.Column(db.String(100), nullable=False)
    RoomNumber = db.Column(db.String(100), nullable=False)
    RoomName = db.Column(db.String(100), nullable=False)
    Area = db.Column(db.Float, nullable=False)
    RoomPopulation = db.Column(db.Integer, nullable=False)
    Comments = db.Column(db.String(250))

    room_type = db.relationship('RoomTypes', backref='room_type', uselist=False, lazy=True)
    ventilation_properties = db.relationship('RoomVentilationProperties', backref='room_ventilation', uselist=False, lazy=True)
    energy_properties = db.relationship('RoomEnergyProperties', backref="room_energy", uselist=False, lazy=True)

class VentilationSystems(db.Model):
    __tablename__ = "VentilationSystems"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    SystemName = db.Column(db.String(30), nullable=False)
    Location = db.Column(db.String(100))
    ServiceArea = db.Column(db.String(250))
    HeatExchange = db.Column(db.String(30))
    AirFlow = db.Column(db.Float)
    AirFlowSupply = db.Column(db.Float)
    AirFlowExtract = db.Column(db.Float)
    SpecialSystem = db.Column(db.String)

    room = db.relationship('RoomVentilationProperties', backref="room", lazy=True)

class RoomVentilationProperties(db.Model):
    __tablename__ = "RoomVentilationProperties"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoomId = db.Column(db.Integer, db.ForeignKey('Rooms.id', ondelete="SET NULL"), nullable=False, unique=True)
    SystemId = db.Column(db.Integer, db.ForeignKey('VentilationSystems.id', ondelete="SET NULL"), nullable=True)
    AirPerPerson = db.Column(db.Float)
    AirPersonSum = db.Column(db.Integer)
    AirEmission = db.Column(db.Float)
    AirEmissionSum = db.Column(db.Float)
    AirProcess = db.Column(db.Float)
    AirMinimum = db.Column(db.Float)
    AirDemand = db.Column(db.Float)
    AirSupply = db.Column(db.Float)
    AirExtract = db.Column(db.Float)
    AirChosen = db.Column(db.Float)
    VentilationPrinciple = db.Column(db.String(50))
    HeatExchange = db.Column(db.String(50))
    RoomControl = db.Column(db.String(50))
    Notes = db.Column(db.String(100))
    DbTechnical = db.Column(db.String(50))
    DbNeighbour = db.Column(db.String(50))
    DbCorridor = db.Column(db.String(50))
    Comments = db.Column(db.String(20))

class BuildingEnergySettings(db.Model):
    __tablename__ = "BuildingEnergySettings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    BuildingID = db.Column(db.Integer, db.ForeignKey('Buildings.id', ondelete="SET NULL"), nullable=False, unique=True)
    # Heating properties
    InsideTemp = db.Column(db.Float)
    VentTemp = db.Column(db.Float)
    Infiltration = db.Column(db.Float)
    UvalueOuterWall = db.Column(db.Float)
    UvalueWindowDoor = db.Column(db.Float)
    UvalueFloorGround = db.Column(db.Float)
    UvalueFloorAir = db.Column(db.Float)
    UvalueRoof = db.Column(db.Float)
    ColdBridge = db.Column(db.Float)
    YearMidTemp = db.Column(db.Float)
    TempFloorAir = db.Column(db.Float)
    Dut = db.Column(db.Float)
    Safety = db.Column(db.Integer)


    room_energy = db.relationship('RoomEnergyProperties', backref='building_energy_settings', lazy=True)


class RoomEnergyProperties(db.Model):
    __tablename__ = "RoomEnergyProperties"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoomId = db.Column(db.Integer, db.ForeignKey('Rooms.id', ondelete="SET NULL"), nullable=False, unique=True)
    BuildingEnergySettings = db.Column(db.Integer, db.ForeignKey('BuildingEnergySettings.id', ondelete="SET NULL"), nullable=False)
    # Heating settings
    OuterWallArea = db.Column(db.Float)
    RoomHeight = db.Column(db.Float)
    WindowDoorArea = db.Column(db.Float)
    InnerWallArea = db.Column(db.Float)
    RoofArea = db.Column(db.Float)
    FloorGroundArea = db.Column(db.Float)
    FloorAirArea = db.Column(db.Float)
    RoomVolume = db.Column(db.Float)
    HeatLossColdBridge = db.Column(db.Float)
    HeatLossTransmission = db.Column(db.Float)
    HeatLossInfiltration = db.Column(db.Float)
    HeatLossVentilation = db.Column(db.Float)
    HeatLossSum = db.Column(db.Float)
    ChosenHeating = db.Column(db.Float)
    HeatSource = db.Column(db.String(50))
    # Cooling settings
    RoomTempSummer = db.Column(db.Float)
    InternalLoadPeople = db.Column(db.Float)
    InternalLoadLight = db.Column(db.Float)
    SunAdition = db.Column(db.Float)
    VentAirTempSummer = db.Column(db.Float)
    SumInternalHeatloadPeople = db.Column(db.Float)
    SumInternalHeatloadLight = db.Column(db.Float)
    InternalHeatloadEquipment = db.Column(db.Float)
    SunAdition = db.Column(db.Float)
    SunReduction = db.Column(db.Float)
    SumInternalHeatLoad = db.Column(db.Float)
    CoolingVentilationAir = db.Column(db.Float)
    CoolingEquipment = db.Column(db.Float)
    CoolingSum = db.Column(db.Float)
    

''' 
Specification tables
'''
class Specifications(db.Model):
    __tablename__ = "Specifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    room_types = db.relationship("RoomTypes", backref="specifications", uselist=False, lazy=True)

class RoomTypes(db.Model):
    __tablename__ = "RoomTypes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specification_id = db.Column(db.Integer, db.ForeignKey("Specifications.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    air_per_person = db.Column(db.Float)
    air_emission = db.Column(db.Float)
    air_process = db.Column(db.Float)
    air_minimum = db.Column(db.Float)
    ventilation_principle = db.Column(db.String(50))
    heat_exchange = db.Column(db.String(50))
    room_control = db.Column(db.String(50))
    notes = db.Column(db.String(100))
    db_technical = db.Column(db.String(50))
    db_neighbour = db.Column(db.String(50))
    db_corridor = db.Column(db.String(50))
    comments = db.Column(db.String(20))
    