from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from config.config import RECORDS_PATH

router = APIRouter()

@router.get("/api/strip_data")
async def get_strip_data():
    json_file_path = os.path.join(RECORDS_PATH ,"StripData.json")
    if not os.path.exists(json_file_path):
        raise HTTPException(status_code=404, detail="record not found")
    
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Seleccionar solo los valores de ejemplo
        return JSONResponse(content=data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error al decodificar el archivo JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo: {str(e)}")