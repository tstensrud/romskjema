from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Project(db.Model):
    __tablename__ = "Projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectNumber = db.Column(db.Integer, nullable=False)
    ProjectName = db.Column(db.String(50), nullable=False)
    ProjectDescription = db.Column(db.String(200))

class Buildings(db.Model):
    __tablename__ = "Buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    BuildingName = db.Column(db.String(100), nullable=False)

class Room(db.Model):
    __tablename__ = "Rooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    BuildingId = db.Column(db.Integer, db.ForeignKey('Buildings.id'), nullable=False)
    RoomType = db.Column(db.String(100), nullable=False)
    Floor = db.Column(db.String(100), nullable=False)
    RoomNumber = db.Column(db.String(100), nullable=False)
    RoomName = db.Column(db.String(100), nullable=False)
    Area = db.Column(db.Integer, nullable=False)
    RoomPopulation = db.Column(db.Integer, nullable=False)

class VentilationProperties(db.Model):
    __tablename__ = "VentilationProperties"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoomId = db.Column(db.Integer, db.ForeignKey('Rooms.id'), nullable=False)
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
    DBCorridor = db.Column(db.String(50))
    System = db.Column(db.String(50))
    Comments = db.Column(db.String(20))


    
