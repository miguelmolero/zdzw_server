import os
import orjson
import shutil
from datetime import datetime
from config.config import RECEIVED_RECORDS_PATH, STORED_RECORDS_PATH
from database.database_conection import SessionLocal
from database.models.RecordDataModel.records_data import RecordsData
from database.models.FactoryDataModel.factory_data import FactoryData
from database.models.DeviceDataModel.device_data import DeviceData
import database.models.RecordDataModel.records_data_database_handler as records_data_handler
import database.models.FactoryDataModel.factory_data_database_handler as factory_data_handler
import database.models.DeviceDataModel.device_data_database_handler as device_data_handler
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
                    print(f"Processing file: {file_name}")
                    raw_data = orjson.loads(file.read())
                    record_raw_data  = RecordRawData.parse_custom(raw_data)
                    metadata = record_raw_data.payload_data.meta_data
                    localization_data = record_raw_data.localization_data

                    json_record_id = metadata.record_id
                    json_timestamp = datetime.fromtimestamp(metadata.timestamp)
                    json_name = metadata.name
                    json_disposition = metadata.disposition
                    json_job_id = metadata.job_id

                    # Insertar en la base de datos si no existe
                    db = SessionLocal()
                    existing_factory = factory_data_handler.SelectByFactoryId(db, FactoryData, localization_data.factory_id)
                    if not existing_factory:
                        new_factory = FactoryData(
                            factory_id = localization_data.factory_id,
                            factory_name = localization_data.factory_name
                        )
                        if not factory_data_handler.InsertFactoryData(db, FactoryData, instance = new_factory):
                            print(f"Error to insert new factory {localization_data.factory_id}")
                            continue
                    
                    existing_device = device_data_handler.GetDeviceByFactoryId(db, DeviceData, localization_data.factory_id)
                    if not existing_device:
                        new_device = DeviceData(
                            device_id = localization_data.device_id,
                            device_name = localization_data.device_name,
                            factory_id = localization_data.factory_id
                        )
                        if not device_data_handler.InsertDeviceData(db, DeviceData, instance = new_device):
                            print(f"Error to insert new device {localization_data.device_id}")
                            continue

                    existing_record = records_data_handler.SelectByRecordId(db, RecordsData, json_record_id, localization_data.factory_id, localization_data.device_id)
                    if existing_record:
                        print(f"The record_id {json_record_id} already exists")
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        continue
                    else:
                        new_inspection = RecordsData(
                            record_id = json_record_id,
                            timestamp = json_timestamp,
                            job_id = json_job_id,
                            job_name = json_name,
                            disposition = json_disposition,
                            factory_id = localization_data.factory_id,
                            device_id = localization_data.device_id
                        )
                        if not records_data_handler.InsertRecord(db, RecordsData, instance = new_inspection):
                            print(f"Error inserting record_id {json_record_id}")
                            continue

                    # Mover el archivo procesado
                    factory_folder = os.path.join(STORED_RECORDS_PATH, str(localization_data.factory_id))
                    os.makedirs(factory_folder, exist_ok=True)
                    device_folder = os.path.join(factory_folder, str(localization_data.device_id))
                    os.makedirs(device_folder, exist_ok=True)
                    destination_folder = os.path.join(device_folder, str(json_record_id))
                    os.makedirs(destination_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(destination_folder, file_name))
                    print(f"Proccessed file: {file_name}")

            except Exception as e:
                print(f"Proccessing error {file_name}: {e}")
            finally:
                db.close()

            # Eliminar el archivo original si aún existe
            if os.path.exists(file_path):
                os.remove(file_path)
