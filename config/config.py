from pathlib import Path
import sys
import secrets

def is_docker():
    return Path("/.dockerenv").exists()

if is_docker():
    BASE_PATH = Path("/app")  # Docker environment
else:
    BASE_PATH = Path(__file__).resolve().parent.parent / "app"  # Local development environment

# Configuración de CORS
CORS_ORIGINS = ["http://localhost:5000"]

# Configuración de la ruta de archivos estáticos
STATIC_FOLDER_PATH = (BASE_PATH / "../static/dist").resolve()

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_PATH = BASE_PATH / "data" / "zdzw.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
RECEIVED_RECORDS_PATH = BASE_PATH / "ReceivedRecords"
RECEIVED_TEMP_RECORDS_PATH = BASE_PATH / "ReceivedTempRecords"
STORED_RECORDS_PATH = BASE_PATH / "RecordsData"