from pydantic import BaseModel
from datetime import datetime 
from typing import Optional, Union

class FiltersPayload(BaseModel):
    current_record_id: Optional[int] = None
    requested_record_id: Optional[int] = None
    start_date: Optional[Union[datetime,int]] = None
    end_date: Optional[Union[datetime, int]] = None
    disposition: Optional[int] = None
    factory_id: Optional[int] = None
    device_id: Optional[int] = None
    is_analysis: Optional[bool] = False