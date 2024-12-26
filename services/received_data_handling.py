import os
import orjson
import shutil
from datetime import datetime
from config.config import RECEIVED_RECORDS_PATH, STORED_RECORDS_PATH
from database.database_conection import SessionLocal
from database.models.RecordDataModel.records_data import RecordsData
import database.models.RecordDataModel.records_data_database_handler as records_data_handler
from models.record_data import RecordRawData


def read_received_data():
    # Check if the received data directory exists
    if not os.path.exists(RECEIVED_RECORDS_PATH):
        os.makedirs(RECEIVED_RECORDS_PATH, exist_ok=True)
        return

    os.makedirs(STORED_RECORDS_PATH, exist_ok=True)

    for file_name in os.listdir(RECEIVED_RECORDS_PATH):
        if file_name.endswith(".json"):
            file_path = os.path.join(RECEIVED_RECORDS_PATH, file_name)

            try:
                # Leer el contenido del archivo JSON
                with open(file_path, "r") as file:
                    raw_data = orjson.loads(file.read())
                    record_raw_data  = RecordRawData.parse_custom(raw_data)
                    metadata = record_raw_data.payload_data.metadata

                    json_record_id = metadata.record_id
                    json_timestamp = datetime.fromtimestamp(metadata.timestamp)
                    json_name = metadata.name
                    json_disposition = metadata.disposition

                    # Insertar en la base de datos si no existe
                    db = SessionLocal()
                    existing_record = records_data_handler.SelectByRecordId(db, RecordsData, json_record_id)

                    if existing_record:
                        print(f"The record_id {json_record_id} already exists")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        continue
                    else:
                        
                        new_inspection = RecordsData(
                            record_id = json_record_id,
                            timestamp = json_timestamp,
                            job_name = json_name,
                            disposition = json_disposition
                        )
                        if not records_data_handler.InsertRecord(db, RecordsData, instance = new_inspection):
                            print(f"Error inserting record_id {json_record_id}")
                            continue

                    # Mover el archivo procesado
                    destination_folder = os.path.join(STORED_RECORDS_PATH, str(json_record_id))
                    os.makedirs(destination_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(destination_folder, file_name))
                    print(f"Archivo procesado: {file_name}")

            except Exception as e:
                print(f"Error procesando {file_name}: {e}")
            finally:
                db.close()

            # Eliminar el archivo original si aún existe
            if os.path.exists(file_path):
                os.remove(file_path)
