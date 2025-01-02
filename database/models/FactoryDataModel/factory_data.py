from database.database_conection import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class FactoryData(Base):
    __tablename__ = "FactoryData"

    id = Column(Integer, primary_key=True, index=True)
    factory_id = Column(Integer, unique=True, nullable=False, index=True)
    factory_name = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())
    # Add more columns as needed