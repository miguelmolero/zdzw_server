from pydantic import BaseModel
from datetime import datetime 
from typing import Optional, Union, Dict, Any
from enum import Enum

class InspectionFilters(BaseModel):
    requested_record_id: Optional[int] = None
    start_date: Optional[Union[datetime,int]] = None
    end_date: Optional[Union[datetime, int]] = None
    disposition: Optional[int] = None
    factory_id: Optional[int] = None
    device_id: Optional[int] = None
    job_id: Optional[int] = None
    is_analysis: Optional[bool] = False

class OrderType(str, Enum):
    ORDER_TYPE_DATE = "date"
    ORDER_TYPE_PASS = "pass"
    ORDER_TYPE_FAIL = "fail"
    ORDER_TYPE_INVALID = "invalid"

class OrderDirection(str, Enum):
    ORDER_DIRECTION_ASCENDING = "asc"
    ORDER_DIRECTION_DESCENDING = "desc"


class OrderFilters(BaseModel):
    order_direction: Optional[str] = None
    order_type: Optional[str] = None

class CurrentRecord(BaseModel):
    factory_id: int
    device_id: int
    record_id: int

class RequestedPayload(BaseModel):
    nav_filters: InspectionFilters
    order_filters: Optional[OrderFilters] = None
    loaded_record: CurrentRecord