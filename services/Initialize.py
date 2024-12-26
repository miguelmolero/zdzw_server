from database.database_initialization import init_db
from services.received_data_handling import read_received_data

def initialize():
    init_db()
    read_received_data()