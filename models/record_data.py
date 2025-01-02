from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Metadata(BaseModel):
    record_id: int
    timestamp: int
    setup_id: int
    job_id: int
    setup_updated_timestamp: int
    name: str
    disposition: int
    is_rotational: bool

class StripData(BaseModel):
    channel_id: int
    gate_id: int
    sample: List[int]
    distance: List[float]
    amplitude: List[float]
    tof: List[float]
    amp_damages: Optional[List[float]] = None
    tof_damages: Optional[List[float]] = None

class RecordData(BaseModel):
    meta_data: Metadata
    strip_data: List[StripData]

class LocalizationData(BaseModel):
    factory_id: int
    factory_name: str
    device_id: int
    device_name: str
class ErrorData(BaseModel):
    code: int
    msg: str
    errors: Optional[List[str]] = None

class RecordRawData(BaseModel):
    success: bool
    error: ErrorData
    payload_data: RecordData
    localization_data: LocalizationData

    @classmethod
    def parse_custom(cls, data: Dict[str, Any]) -> "RecordRawData":
        # Adaptar el JSON al modelo esperado
        payload = data.get("payload", {})
        strip_data = payload.get("strip_data", [])
        localization_data = data.get("localization_info", {})

        # Transformar el JSON para que coincida con la estructura esperada
        transformed_data = {
            "success": data.get("success", False),
            "error": {
                "code": data.get("error", {}).get("code", 0),
                "msg": data.get("error", {}).get("msg", ""),
                "errors": data.get("error", {}).get("errors"),
            },
            "payload_data": {
                "meta_data": {
                    "record_id": payload.get("record_id"),
                    "timestamp": payload.get("timestamp"),
                    "setup_id": payload.get("setup_id"),
                    "job_id": payload.get("job_id"),
                    "setup_updated_timestamp": payload.get("setup_updated_timestamp"),
                    "name": payload.get("name"),
                    "disposition": payload.get("disposition"),
                    "is_rotational": payload.get("is_rotational"),
                },
                "strip_data": [
                    {
                        "channel_id": strip.get("channel_id"),
                        "gate_id": strip.get("gate_id"),
                        "sample": strip.get("sample", []),
                        "distance": strip.get("distance", []),
                        "amplitude": strip.get("amplitude", []),
                        "tof": strip.get("tof", []),
                        "amp_damages": strip.get("amp_damages", []),
                        "tof_damages": strip.get("tof_damages", []),
                    }
                    for strip in strip_data
                ],
            },
            "localization_data": {
                "factory_id": localization_data.get("factory_id"),
                "factory_name": localization_data.get("factory_name"),
                "device_id": localization_data.get("device_id"),
                "device_name": localization_data.get("device_name"),
            },
        }

        # Validar y crear una instancia del modelo
        return cls(**transformed_data)