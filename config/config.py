import os
import sys

# Determina si la aplicación está empaquetada con PyInstaller
def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.abspath(os.path.dirname(__file__))

# Configuración de CORS
CORS_ORIGINS = ["http://localhost:5000"]

# Configuración de la ruta de archivos estáticos
BASE_PATH = get_base_path()
STATIC_FOLDER_PATH = os.path.join(BASE_PATH, 'static/dist')
