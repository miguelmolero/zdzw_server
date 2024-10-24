from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()

@router.get("/strip_data")
async def get_strip_data():
    json_file_path = Path(__file__).parent.parent / "data" / "sample.json"
    if not json_file_path.exists():
        raise HTTPException(status_code=404, detail="JSON file not found")
    
    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)
            # Seleccionar solo los valores de ejemplo
            selected_data = [item["value"] for item in data["records"]]
            return {"selected_data": selected_data}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error parsing JSON file")