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
    ProjectDescription = db.Column(db.Text)
    Specification = db.Column(db.String(50))

    buildings = db.relationship('Buildings', backref='project', uselist=False, lazy=True)
    systems = db.relationship('VentilationSystems', backref='project', uselist=False, lazy=True)
    


class Buildings(db.Model):
    __tablename__ = "Buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    BuildingName = db.Column(db.String(100), nullable=False)

    rooms = db.relationship('Rooms', backref='building', lazy=True)


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

    ventilation_properties = db.relationship('RoomVentilationProperties', backref='rooms', uselist=False, lazy=True)

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
    RoomId = db.Column(db.Integer, db.ForeignKey('Rooms.id'), nullable=False, unique=True) # add ondelete="SET NULL"
    SystemId = db.Column(db.Integer, db.ForeignKey('VentilationSystems.id'), nullable=True) # add ondelete="SET NULL"
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

