from fastapi import APIRouter, HTTPException, UploadFile, File
from config.config import RECEIVED_RECORDS_PATH, RECEIVED_TEMP_RECORDS_PATH
from pathlib import Path
import zipfile
import shutil

router = APIRouter()

@router.post("/api/received_records")
async def get_received_records(file: UploadFile = File(...)):
    #print(f"get_received_records***************************************************")
    print(f"Received file: {file.filename}")
    if not RECEIVED_TEMP_RECORDS_PATH.exists():
        RECEIVED_TEMP_RECORDS_PATH.mkdir(parents=True, exist_ok=True)
    temp_file_path = RECEIVED_TEMP_RECORDS_PATH / file.filename
    with temp_file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    file_extension = temp_file_path.suffix.lower()

    try:
        if file_extension == ".zip":
            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                zip_ref.extractall(RECEIVED_RECORDS_PATH)
            mensaje = "ZIP file correctly extracted."

        elif file_extension == ".json":
            final_json_path = RECEIVED_RECORDS_PATH / file.filename
            temp_file_path.replace(final_json_path)
            mensaje = "JSON file correctly saved."

        else:
            raise HTTPException(status_code=400, detail="Not a valid file extension.")

        return {
            "message": mensaje,
            "filename": file.filename,
            "destination_folder": str(RECEIVED_RECORDS_PATH)
        }

    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Not valid Zip file.")

    finally:
        if RECEIVED_TEMP_RECORDS_PATH.exists():
            shutil.rmtree(RECEIVED_TEMP_RECORDS_PATH)
        RECEIVED_TEMP_RECORDS_PATH.mkdir(parents=True, exist_ok=True)
