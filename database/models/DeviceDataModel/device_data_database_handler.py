from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type
from sqlalchemy.ext.declarative import DeclarativeMeta

def GetFactoryId(db: Session, model: Type[DeclarativeMeta], device_id: int):
    return db.query(model).filter(model.device_id == device_id).first().factory_id

def GetDeviceName(db: Session, model: Type[DeclarativeMeta], device_id: int) -> str:
    return db.query(model).filter(model.device_id == device_id).first().device_name

def GetDeviceByFactoryId(db: Session, model: Type[DeclarativeMeta], factory_id: int) -> bool:
    return True if db.query(model).filter(model.factory_id == factory_id).first() != None else False

def InsertDeviceData(db: Session, model: Type[DeclarativeMeta], **kwargs) -> bool:
    try:
        instance = None
        for value in kwargs.values():
            if isinstance(value, model):
                instance = value
                break
        if instance is None:
            instance = model(**kwargs)
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error to insert new device: {e}")
        return False