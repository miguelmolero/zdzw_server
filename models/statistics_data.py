from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class StatsData(BaseModel):
    id: int
    total_count: int
    pass_count: int
    fail_count: int
    invalid_count: int
    pass_percentage: float
    fail_percentage: float
    invalid_percentage: float

class FactoryStatsData(BaseModel):
    factory_data: StatsData
    device_stats: List[StatsData]

class StatisticsData(BaseModel):
    factory_stats: List[FactoryStatsData] 

    @classmethod
    def encode_custom(cls, data: "StatisticsData") -> Dict[str, Any]:
        return {
            "factory_stats": [
                {
                    "id": factory.factory_data.id,
                    "total_count": factory.factory_data.total_count,
                    "pass_count": factory.factory_data.pass_count,
                    "fail_count": factory.factory_data.fail_count,
                    "invalid_count": factory.factory_data.invalid_count,
                    "pass_percentage": factory.factory_data.pass_percentage,
                    "fail_percentage": factory.factory_data.fail_percentage,
                    "invalid_percentage": factory.factory_data.invalid_percentage,
                    "device_stats": [
                        {
                            "id": device.id,
                            "total_count": device.total_count,
                            "pass_count": device.pass_count,
                            "fail_count": device.fail_count,
                            "invalid_count": device.invalid_count,
                            "pass_percentage": device.pass_percentage,
                            "fail_percentage": device.fail_percentage,
                            "invalid_percentage": device.invalid_percentage
                        }
                        for device in factory.device_stats
                    ]
                }
                for factory in data.factory_stats
            ]
        }