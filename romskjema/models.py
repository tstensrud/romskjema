from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

'''
User table
'''
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)

'''
Project-specific tables
'''
class Projects(db.Model):
    __tablename__ = "Projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectNumber = db.Column(db.Integer, nullable=False)
    ProjectName = db.Column(db.String(50), nullable=False)
    ProjectDescription = db.Column(db.String(200))
    Specification = db.Column(db.String(50))

    buildings = db.relationship('Buildings', backref='project', uselist=False, lazy=True)

    def set_project_number(self, project_number: str) -> None:
        self.ProjectNumber = project_number
    def set_project_name(self, project_name: str) -> None:
        self.ProjectName = project_name
    def set_project_description(self, description: str) -> None:
        self.ProjectDescription = description
    
    def get_specifictaion(self) -> str:
        return self.Specification

class Buildings(db.Model):
    __tablename__ = "Buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    BuildingName = db.Column(db.String(100), nullable=False)

    rooms = db.relationship('Rooms', backref='building', lazy=True)

    def set_building_name(self, name: str) -> None:
        self.BuildingName = name

class Rooms(db.Model):
    __tablename__ = "Rooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BuildingId = db.Column(db.Integer, db.ForeignKey('Buildings.id'), nullable=False)
    RoomType = db.Column(db.String(100), nullable=False)
    Floor = db.Column(db.String(100), nullable=False)
    RoomNumber = db.Column(db.String(100), nullable=False)
    RoomName = db.Column(db.String(100), nullable=False)
    Area = db.Column(db.Float, nullable=False)
    RoomPopulation = db.Column(db.Integer, nullable=False)
    Comments = db.Column(db.String(250))

    ventilation_properties = db.relationship('VentilationProperties', backref='rooms', uselist=False, lazy=True)

    def set_room_number(self, room_number: str) -> None:
        self.RoomNumber = room_number
    def set_room_name(self, room_name: str) -> None:
        self.RoomName = room_name
    def set_area(self, area: float) -> None:
        self.Area = area
    def set_population(self, population: int) -> None:
        self.RoomPopulation = population
    def set_comment(self, comment: str) -> None:
        self.Comments = comment

class VentilationProperties(db.Model):
    __tablename__ = "VentilationProperties"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoomId = db.Column(db.Integer, db.ForeignKey('Rooms.id'), nullable=False, unique=True)
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
    System = db.Column(db.String(50))
    Comments = db.Column(db.String(20))

    def __init__(self, RoomId, area=None, AirPerPerson=None, AirEmission=None, 
                 AirProcess=None, AirMinimum=None, AirSupply=None, AirExtract=None, 
                 VentilationPrinciple=None, HeatExchange=None, RoomControl=None, 
                 Notes=None, DbTechnical=None, DbNeighbour=None, DBCorridor=None, System=None, 
                 Comments=None):
        self.RoomId = RoomId
        self.area = area
        self.AirPerPerson = AirPerPerson
        self.AirEmission = AirEmission
        self.AirProcess = AirProcess
        self.AirMinimum = AirMinimum
        self.AirSupply = AirSupply
        self.AirExtract = AirExtract  
        self.VentilationPrinciple = VentilationPrinciple
        self.HeatExchange = HeatExchange
        self.RoomControl = RoomControl
        self.Notes = Notes
        self.DbTechnical = DbTechnical
        self.DbNeighbour = DbNeighbour
        self.DbCorridor = DBCorridor
        self.System = System
        self.Comments = Comments
        self.AirPersonSum = 0.0
        self.AirEmissionSum = 0.0
        self.AirDemand = 0.0
        self.AirChosen = 0.0

''' 
Specification tables
'''
class Specifications(db.Model):
    __tablename__ = "Specifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    room_types = db.relationship("RoomTypes", backref="Specifications", uselist=False, lazy=True)

class RoomTypes(db.Model):
    __tablename__ = "RoomTypes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    specification_id = db.Column(db.Integer, db.ForeignKey("Specifications.id"), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    room_data = db.relationship("RoomDataVentilation", uselist=False, lazy=True)

class RoomDataVentilation(db.Model):
    __tablename__ = "RoomDataVentilation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey("RoomTypes.id"), nullable=False, unique=True)
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

