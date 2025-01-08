from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, List, Optional
from sqlalchemy.ext.declarative import DeclarativeMeta
from models.filter_payload import InspectionFilters

def SelectByFactoryId(db: Session, model: Type[DeclarativeMeta], factory_id: int) -> bool:
    return True if db.query(model).filter(model.factory_id == factory_id).first() != None else False

def GetFactoryName(db: Session, model: Type[DeclarativeMeta], factory_id: int) -> str:
    return db.query(model).filter(model.factory_id == factory_id).first().factory_name

def GetFactories(db: Session, model: Type[DeclarativeMeta], filters: InspectionFilters ) -> Optional[List[int]]:
    start_date = filters.start_date
    end_date = filters.end_date
    factory_id = filters.factory_id
    job_id = filters.job_id

    print(f"Filters: {filters}")

    query = db.query(model.factory_id)

    if factory_id != -1:
        query = query.filter(model.factory_id == factory_id)
    if job_id != -1:
        query = query.filter(model.job_id == job_id)
    if start_date != -1 and end_date != -1:
        query = (
            query.filter(model.timestamp >= start_date)
            .filter(model.timestamp <= end_date)
        )
    return [row[0] for row in query.all()]

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