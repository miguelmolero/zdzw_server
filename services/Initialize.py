from database.database_initialization import init_db
from services.received_data_handling import sync_read_received_data
from config.config import STATIC_FOLDER_PATH
import os

def initialize():
    init_db()
    sync_read_received_data()