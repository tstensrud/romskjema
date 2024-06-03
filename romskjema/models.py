from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)

class Projects(db.Model):
    __tablename__ = "Projects"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectNumber = db.Column(db.Integer, nullable=False)
    ProjectName = db.Column(db.String(50), nullable=False)
    ProjectDescription = db.Column(db.String(200))

    buildings = db.relationship('Buildings', backref='projects', lazy=True)

    def set_project_number(self, project_number: str) -> None:
        self.ProjectNumber = project_number
    def set_project_name(self, project_name: str) -> None:
        self.ProjectName = project_name
    def set_project_description(self, description: str) -> None:
        self.ProjectDescription = description
    

class Buildings(db.Model):
    __tablename__ = "Buildings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProjectId = db.Column(db.Integer, db.ForeignKey('Projects.id'), nullable=False)
    BuildingName = db.Column(db.String(100), nullable=False)

    rooms = db.relationship('Rooms', backref='buildings', lazy=True)

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

    ventilation_properties = db.relationship('VentilationProperties', backref='rooms', lazy=True)

    def set_room_number(self, room_number: str) -> None:
        self.RoomNumber = room_number
    def set_room_name(self, room_name: str) -> None:
        self.RoomName = room_name
    def set_area(self, area: float) -> None:
        self.Area = area
    def set_population(self, population: int) -> None:
        self.RoomPopulation = population

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

    '''
    Calculate sums and air flow / m2
    '''
    def set_air_person_sum(self, population: int) -> None:
        sum = self.AirPerPerson * population
        self.AirPersonSum = round(sum, 1)
        self.set_air_demand()
    
    def set_emission_sum(self, area: float) -> None:
        sum = self.AirEmission * area
        self.AirEmissionSum = round(sum, 1)
        self.set_air_demand()
    
    def set_air_demand(self) -> None:
        demand = self.AirPersonSum + self.AirEmissionSum + self.AirProcess
        self.AirDemand = round(demand, 1)
    
    def set_air_chosen(self, area: float) -> None:
        chosen = self.AirSupply / area
        self.AirChosen = round(chosen, 1)
    
    '''
    Change air flow values
    '''
    def set_air_supply(self, supply: float, area: float) -> None:
        self.AirSupply = round(supply, 1)
        self.set_air_chosen(area)

    def set_air_extract(self, extract: float) -> None:
        self.AirExtract = round(extract, 1)
    
    def set_process(self, process: float) -> None:
        self.AirProcess = round(process, 1)
        self.set_air_demand()

    def set_system(self, system_number: str) -> None:
        self.System = system_number
    def set_comment(self, comment: str) -> None:
        self.Comments = comment

    
