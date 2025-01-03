from pydantic import BaseModel
from datetime import datetime 
from typing import Optional, Union, Dict, Any

class InspectionFilters(BaseModel):
    requested_record_id: Optional[int] = None
    start_date: Optional[Union[datetime,int]] = None
    end_date: Optional[Union[datetime, int]] = None
    disposition: Optional[int] = None
    factory_id: Optional[int] = None
    device_id: Optional[int] = None
    is_analysis: Optional[bool] = False

class CurrentRecord(BaseModel):
    factory_id: int
    device_id: int
    record_id: int

class RequestedPayload(BaseModel):
    nav_filters: InspectionFilters
    loaded_record: CurrentRecord