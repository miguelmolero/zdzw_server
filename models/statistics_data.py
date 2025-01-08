from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class StatsData(BaseModel):
    id: int
    total_count: int
    pass_count: int
    fail_count: int
    invalid_count: int
    pass_rate: float
    fail_rate: float
    invalid_rate: float

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
                    "pass_rate": factory.factory_data.pass_rate,
                    "fail_rate": factory.factory_data.fail_rate,
                    "invalid_rate": factory.factory_data.invalid_rate,
                    "device_stats": [
                        {
                            "id": device.id,
                            "total_count": device.total_count,
                            "pass_count": device.pass_count,
                            "fail_count": device.fail_count,
                            "invalid_count": device.invalid_count,
                            "pass_rate": device.pass_rate,
                            "fail_rate": device.fail_rate,
                            "invalid_rate": device.invalid_rate
                        }
                        for device in factory.device_stats
                    ]
                }
                for factory in data.factory_stats
            ]
        }