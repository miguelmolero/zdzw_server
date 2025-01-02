from database.database_conection import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class DeviceData(Base):
    __tablename__ = "DeviceData"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, nullable=False, index=True)
    device_name = Column(String, index=True)
    factory_id = Column(Integer, index=True)
    created_at = Column(DateTime, server_default=func.now())
    # Add more columns as needed