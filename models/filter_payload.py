from pydantic import BaseModel
from datetime import datetime 
from typing import Optional

class FiltersPayload(BaseModel):
    current_record_id: Optional[int] = None
    requested_record_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    disposition: Optional[int] = None