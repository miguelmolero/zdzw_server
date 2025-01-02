from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Type, List, Optional, Dict
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
from models.filter_payload import FiltersPayload
from database.database_conection import Base

# Select by Record ID
def SelectByRecordId(db: Session, model: Type[DeclarativeMeta], record_id: int, factory_id: int, device_id: int) -> bool:
    query = (
        db.query(model)
        .filter(model.record_id == record_id)
        .filter(model.factory_id == factory_id)
        .filter(model.device_id == device_id)
        .first()
    )
    return True if query != None else False

# Select by Disposition
def SelectByDisposition(db: Session, model: Type[DeclarativeMeta], disposition: int):
    return db.query(model).filter(model.disposition == disposition).first()

def SelectRecordIdByTimestamp(db: Session, model: Type[DeclarativeMeta], start_date: datetime, end_date: datetime) -> Optional[List[int]]:
    return (
        db.query(model.record_id)
        .filter(model.timestamp >= start_date)
        .filter(model.timestamp <= end_date)
        .all()
    )

def SelectFirstAndLast(db: Session, model: Type[DeclarativeMeta], start_date: datetime, end_date: datetime, disposition: int, navigation: str) -> Optional[Dict[str, DeclarativeMeta]]:
    
    if start_date is -1 and end_date is -1 and disposition is -1:
        return ({
            "first": db.query(model).order_by(model.timestamp.asc()).first(),
            "last": db.query(model).order_by(model.timestamp.desc()).first()
        })
    elif start_date is -1 and end_date is -1 and disposition is not -1:
        return ({
            "first": db.query(model).filter(model.disposition == disposition).order_by(model.timestamp.asc()).first(),
            "last": db.query(model).filter(model.disposition == disposition).order_by(model.timestamp.desc()).first()
        })
    elif start_date is not -1 and end_date is not -1 and disposition is -1:
        return ({
            "first": db.query(model).filter(model.timestamp >= start_date).filter(model.timestamp <= end_date).order_by(model.timestamp.asc()).first(),
            "last": db.query(model).filter(model.timestamp >= start_date).filter(model.timestamp <= end_date).order_by(model.timestamp.desc()).first()
        })
    else:
        query = (
            db.query(model)
            .filter(model.timestamp >= start_date)
            .filter(model.timestamp <= end_date)
            .filter(model.disposition == disposition)
        )
        return ({
            "first": query.order_by(model.timestamp.asc()).first(),
            "last": query.order_by(model.timestamp.desc()).first()
        })
    
def SelectAdjacentRecord(db: Session, model: Type[DeclarativeMeta], filters: FiltersPayload, navigation: str) -> Optional[DeclarativeMeta]:
    disposition = filters.disposition
    record_id = filters.current_record_id
    factory_id = filters.factory_id
    device_id = filters.device_id
    
    current_range = []
    if disposition is not -1:
        current_range = (
            db.query(model)
            .filter(model.disposition == disposition)
            .order_by(model.timestamp.asc())
            .all()
        )
    else:
        current_range = db.query(model).order_by(model.timestamp.asc()).all()

    for idx, record in enumerate(current_range):
        if record.record_id == record_id and record.factory_id == factory_id and record.device_id == device_id:
            if navigation == "next" and idx + 1 < len(current_range):
                return current_range[idx + 1]
            elif navigation == "previous" and idx - 1 >= 0:
                return current_range[idx - 1]
            break

# Insert a new row
def InsertRecord(db: Session, model: Type[DeclarativeMeta], **kwargs) -> bool:
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
        print(f"Error to insert new record: {e}")
        return False