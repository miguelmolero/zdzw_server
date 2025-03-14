from pydantic import BaseModel
from typing import List

class DefectItem(BaseModel):
    name: str
    start_index: int
    end_index: int
    start_feature_value: float
    end_feature_value: float
    risk_level: int


class DefectsData(BaseModel):
    defects_amp : List[DefectItem]
    defects_tof : List[DefectItem]