
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
def get_building_heating_settings(building_id: int) -> models.BuildingHeatingSettings:
    settings = db.session.query(models.BuildingHeatingSettings).join(models.Buildings).filter(models.Buildings.id == building_id).first()
    return settings