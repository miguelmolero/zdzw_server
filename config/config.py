from pathlib import Path
import sys
import secrets

# Determina si la aplicación está empaquetada con PyInstaller
def get_base_path():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent

# Configuración de CORS
CORS_ORIGINS = ["http://localhost:5000"]

# Configuración de la ruta de archivos estáticos
BASE_PATH = get_base_path()
STATIC_FOLDER_PATH = (BASE_PATH / "../static/dist").resolve()

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./zdzw.db"  # database URL
RECEIVED_RECORDS_PATH = (BASE_PATH / "../../ReceivedRecords").resolve()
RECEIVED_TEMP_RECORDS_PATH = (BASE_PATH / "../../ReceivedTempRecords").resolve()
STORED_RECORDS_PATH = (BASE_PATH / "../../RecordsData").resolve()
