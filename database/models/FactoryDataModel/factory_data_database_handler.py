from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, List, Optional
from sqlalchemy.ext.declarative import DeclarativeMeta

def SelectByFactoryId(db: Session, model: Type[DeclarativeMeta], factory_id: int) -> bool:
    return True if db.query(model).filter(model.factory_id == factory_id).first() != None else False

def GetFactoryName(db: Session, model: Type[DeclarativeMeta], factory_id: int) -> str:
    return db.query(model).filter(model.factory_id == factory_id).first().factory_name

def GetFactories(db: Session, model: Type[DeclarativeMeta]) -> Optional[List[int]]:
    return [row[0] for row in db.query(model.factory_id).all()]

def InsertFactoryData(db: Session, model: Type[DeclarativeMeta], **kwargs) -> bool:
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
        print(f"Error to insert new factory: {e}")
        return False