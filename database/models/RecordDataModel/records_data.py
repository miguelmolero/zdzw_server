from sqlalchemy import Column, Integer, String, DateTime, func
from database.database_conection import Base  # import base model

class RecordsData(Base):
    __tablename__ = "RecordsData"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime, index=True)
    job_name = Column(String, index=True)
    disposition = Column(Integer, index=True)
    factory_id = Column(Integer, index=True)
    device_id = Column(Integer, index=True)
    created_at = Column(DateTime, server_default=func.now())
    # Add more columns as needed