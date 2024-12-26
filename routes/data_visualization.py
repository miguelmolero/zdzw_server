from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import orjson
import os
from pathlib import Path
from datetime import datetime
from config.config import STORED_RECORDS_PATH, BASE_PATH
from models.filter_payload import FiltersPayload
from database.database_conection import SessionLocal
from database.models.RecordData.records_data_database_handler import SelectFirstAndLast, SelectAdjacentRecord
from database.models.RecordData.records_data import RecordsData

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
    print(navigation)
    print(payload_data)

    filter_by_date = False
    filter_by_disposition = False
    if payload_data.start_date != -1:
        filter_by_date = True
        if payload_data.end_date == -1:
            payload_data.end_date = datetime.now()
    if payload_data.disposition != -1:
        filter_by_disposition = True

    init_data = payload_data.start_date
    end_data = payload_data.end_date
    disposition = payload_data.disposition

    db = SessionLocal()

    match navigation:
        case "first" | "last":
            # edge_data = {}
            edge_data = SelectFirstAndLast(db, RecordsData, init_data, end_data, disposition, navigation)
            if (navigation == "first"):
                records = edge_data["first"]
            else:
                records = edge_data["last"]
            json_file_path = os.path.join(STORED_RECORDS_PATH, str(records.record_id))
            try:
                folder = Path(json_file_path)
                json_file = list(folder.glob("*.json"))[0]
                if not json_file.exists():
                    raise HTTPException(status_code=404, detail="record not found")
                with open(json_file, "r", encoding="utf-8") as file:
                    data = orjson.loads(file.read())
                    payload_to_send = {
                        "data": data,
                        "max_record_id": edge_data["last"].record_id,
                        "min_record_id": edge_data["first"].record_id
                    }
                    return JSONResponse(content=payload_to_send)
            except orjson.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Error to decode JSON file")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error to read file: {str(e)}")
        case "previous" | "next":
            adjacent_record_id = SelectAdjacentRecord(db, RecordsData, payload_data.current_record_id, disposition, navigation)
            json_file_path = os.path.join(STORED_RECORDS_PATH, str(adjacent_record_id))
            try:
                folder = Path(json_file_path)
                json_file = list(folder.glob("*.json"))[0]
                if not json_file.exists():
                    raise HTTPException(status_code=404, detail="record not found")
                with open(json_file, "r", encoding="utf-8") as file:
                    data = orjson.loads(file.read())
                    payload_to_send = data
                    return JSONResponse(content=payload_to_send)
            except orjson.JSONDecodeError:
                raise HTTPException(status_code=500, detail="Error to decode JSON file")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error to read file: {str(e)}")