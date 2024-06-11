
from sqlalchemy import func, and_
from . import models, db
from flask_login import login_required
import math
from . import globals

@login_required
def set_up_heating_settings_building(project_id: int, building_id: int) -> bool:
    building_settings = models.BuildingHeatingSettings(ProjectId = project_id,
                                                       BuildingID = building_id,
                                                       InsideTemp = 1.0,
                                                       VentTemp = 1.0,
                                                       Infiltration = 1.0,
                                                       UvalueOuterWall = 1.0,
                                                       UvalueWindowDoor = 1.0,
                                                       UvalueFloorGround = 1.0,
                                                       UvalueFloorAir = 1.0,
                                                       UvalueRoof = 1.0,
                                                       ColdBridge = 1.0,
                                                       YearMidTemp = 1.0,
                                                       TempFloorAir = 1.0,
                                                       Safety=10)
    try:
        db.session.add(building_settings)
        db.session.commit()
        return True
    except Exception as e:
        globals.log(f"set up heating settings building: {e}")
        db.session.rollback()
        return False

@login_required
def new_room_heating_props(project_heating_settings_id: int, room_id: int) -> bool:
    val = 0.1
    new_room = models.RoomHeatingProperties(RoomId=room_id,
                                            ProjectHeatingSettings=project_heating_settings_id,
                                            OuterWallArea = val,
                                            RoomHeight=val,
                                            WindowDoorArea=val,
                                            InnerWallArea=val,
                                            RoofArea=val,
                                            FloorGroundArea=val,
                                            FloorAirArea=val,
                                            RoomVolume=val,
                                            HeatLossColdBridge=val,
                                            HeatLossTransmission=val,
                                            HeatLossInfiltration=val,
                                            HeatLossVentilation=val,
                                            HeatLossSum=val,
                                            ChosenHeating=val,
                                            HeatSource="",
                                            Comment="")
    try:
        db.session.add(new_room)
        db.session.commit()
        return True
    except Exception as e:
        globals.log(f"new room heating props: {e}")
        db.session.rollback()
        return False

@login_required
def get_heating_settings_all_buildings(project_id: int):
    heating_settings = db.session.query(models.BuildingHeatingSettings).join(models.Projects).filter(models.BuildingHeatingSettings.ProjectId == project_id).all()
    return heating_settings

@login_required
def get_building_heating_settings(building_id: int) -> models.BuildingHeatingSettings:
    settings = db.session.query(models.BuildingHeatingSettings).join(models.Buildings).filter(models.Buildings.id == building_id).first()
    return settings