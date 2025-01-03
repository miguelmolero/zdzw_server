from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import orjson
import os
from pathlib import Path
from datetime import datetime
from typing import List
from config.config import STORED_RECORDS_PATH, BASE_PATH
from models.filter_payload import FiltersPayload
from models.record_data import RecordRawData
from models.statistics_data import StatisticsData, FactoryStatsData, StatsData
from database.database_conection import SessionLocal
from database.models.RecordDataModel.records_data import RecordsData
from database.models.FactoryDataModel.factory_data import FactoryData
from database.models.DeviceDataModel.device_data import DeviceData
from database.models.RecordDataModel import records_data_database_handler as record_data_handler
from database.models.FactoryDataModel import factory_data_database_handler as factory_data_handler
from database.models.DeviceDataModel import device_data_database_handler as device_data_handler
from services.get_filtered_data import get_filtered_data

router = APIRouter()

@router.get("/api/strip_data")
async def get_strip_data():
    json_file_path = os.path.join(STORED_RECORDS_PATH ,"StripData.json")
    print("/api/strip_data", json_file_path)
    print("BASE PATH", BASE_PATH)
    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail="record not found")
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = orjson.loads(file.read())
            # Seleccionar solo los valores de ejemplo
        return JSONResponse(content=data)
    except orjson.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error al decodificar el archivo JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")
    
@router.get("/api/stripchart/{record_id}")
async def get_strip_chart(record_id: int):
    json_file_path = os.path.join(STORED_RECORDS_PATH, str(record_id))
    try:
        folder = Path(json_file_path)
        json_file = list(folder.glob("*.json"))[0]
        if not json_file.exists():
            raise HTTPException(status_code=404, detail="record not found")
        with open(json_file, "r", encoding="utf-8") as file:
            data = orjson.loads(file.read())
            return JSONResponse(content=data)
    except orjson.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error to decode JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error to read file: {str(e)}")
    
@router.post("/api/stripchart/{navigation}")
async def post_strip_chart(navigation: str, payload_data: FiltersPayload):
    #print("@router.post)", navigation)
    #print("@router.post)", payload_data)

    if payload_data.start_date != -1:
        if payload_data.end_date == -1:
            payload_data.end_date = datetime.now()

    init_data = payload_data.start_date
    end_data = payload_data.end_date
    disposition = payload_data.disposition
    is_analysis = payload_data.is_analysis

    db = SessionLocal()

    match navigation:
        case "first" | "last":
            # edge_data = {}
            edge_data = record_data_handler.SelectFirstAndLast(db, RecordsData, init_data, end_data, disposition, navigation)
            if (navigation == "first"):
                records = edge_data["first"]
            else:
                records = edge_data["last"]
            file_path = str(records.factory_id) + "/" + str(records.device_id) + "/" + str(records.record_id) 
            json_file_path = os.path.join(STORED_RECORDS_PATH, file_path)
            try:
                folder = Path(json_file_path)
                json_file = list(folder.glob("*.json"))[0]
                if not json_file.exists():
                    raise HTTPException(status_code=404, detail="record not found")
                with open(json_file, "r", encoding="utf-8") as file:
                    data = orjson.loads(file.read())
                    parsed_data = RecordRawData.parse_custom(data)
                    if is_analysis:
                        filtered_data = get_filtered_data(parsed_data)
                    payload_to_send = {
                        "data": filtered_data.model_dump() if is_analysis else parsed_data.model_dump(),
                        "max_record": {
                            "factory_id": edge_data["last"].factory_id,
                            "device_id": edge_data["last"].device_id,
                            "record_id": edge_data["last"].record_id
                        },
                        "min_record": {
                            "factory_id": edge_data["first"].factory_id,
                            "device_id": edge_data["first"].device_id,
                            "record_id": edge_data["first"].record_id
                        }
                    }
                    return JSONResponse(content=payload_to_send)
            except orjson.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Error to decode JSON file")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error to read file: {str(e)}")
        case "previous" | "next":
            adjacent_record = record_data_handler.SelectAdjacentRecord(db, RecordsData, payload_data, navigation)
            record_path = str(adjacent_record.factory_id) + "/" + str(adjacent_record.device_id) + "/" + str(adjacent_record.record_id)
            json_file_path = os.path.join(STORED_RECORDS_PATH, record_path)
            try:
                folder = Path(json_file_path)
                json_file = list(folder.glob("*.json"))[0]
                if not json_file.exists():
                    raise HTTPException(status_code=404, detail="record not found")
                with open(json_file, "r", encoding="utf-8") as file:
                    data = orjson.loads(file.read())
                    parsed_data = RecordRawData.parse_custom(data)
                    if is_analysis:
                        filtered_data = get_filtered_data(parsed_data)
                    payload_to_send = {
                        "data": filtered_data.model_dump() if is_analysis else  parsed_data.model_dump(),
                    }
                    return JSONResponse(content=payload_to_send)
            except orjson.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Error to decode JSON file")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error to read file: {str(e)}")
            
@router.post("/api/statistics")
async def post_statistics(payload_data: FiltersPayload):
    init_data = payload_data.start_date
    end_data = payload_data.end_date
    disposition = payload_data.disposition
    factory_id = payload_data.factory_id
    device_id = payload_data.device_id
    is_analysis = payload_data.is_analysis
    
    db = SessionLocal()

    statistics_data = StatisticsData(factory_stats=[])
    factory_stats : List[FactoryStatsData] = []
    factories = []
    if factory_id == -1:
        factories = factory_data_handler.GetFactories(db, FactoryData)
    else:
        if not factory_data_handler.SelectByFactoryId(db, FactoryData, factory_id): 
            return JSONResponse(content={"error": "Factory not found"})
        else:
            factories.append(factory_id)

    for factory in factories:
        devices_stats : List[StatsData] = []
        factory_data : StatsData
        if device_id == -1:
            devices_stats = record_data_handler.get_device_stats(db, RecordsData, factory)
        else:
            if not device_data_handler.GetDeviceByFactoryId(db, DeviceData, factory_id):
                return JSONResponse(content={"error": "Device not found"})
            else:
                device_data = StatsData(record_data_handler.get_device_stats(db, RecordsData, factory, device_id)[0])
                devices_stats.append(device_data)
        factory_data = record_data_handler.get_factory_stats(db, RecordsData, factory)
        factory_stats.append(FactoryStatsData(factory_data=factory_data, device_stats=devices_stats))
        
    statistics_data.factory_stats = factory_stats
    payload_to_send = {
        "data": StatisticsData.encode_custom(statistics_data)
    }
    return JSONResponse(content=payload_to_send)