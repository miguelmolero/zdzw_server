from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import func, case
from typing import Type, List, Optional, Dict
from datetime import datetime
from models.filter_payload import RequestedPayload, InspectionFilters, CurrentRecord
from models.statistics_data import StatsData
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

def SelectFirstAndLast(db: Session, model: Type[DeclarativeMeta], filters : InspectionFilters) -> Optional[Dict[str, DeclarativeMeta]]:
    
    start_date = filters.start_date
    end_date = filters.end_date
    disposition = filters.disposition
    factory_id = filters.factory_id
    device_id = filters.device_id
    job_id = filters.job_id

    print("FILTERS JOB ID", job_id)

    query = db.query(model)

    if factory_id != -1:
        query = query.filter(model.factory_id == factory_id)
    if device_id != -1:
        query = query.filter(model.device_id == device_id)
    if disposition != -1:
        query = query.filter(model.disposition == disposition)
    if job_id != -1:
        query = query.filter(model.job_id == job_id)
    if start_date != -1 and end_date != -1:
        query = query.filter(model.timestamp >= start_date).filter(model.timestamp <= end_date)

    

    return ({
        "first": query.order_by(model.timestamp.asc()).first(),
        "last": query.order_by(model.timestamp.desc()).first()
    })

def GetFirstTimestamp(db: Session, model: Type[DeclarativeMeta]) -> Optional[datetime]:
    return db.query(func.min(model.timestamp)).first()
    
def SelectAdjacentRecord(db: Session, model: Type[DeclarativeMeta], filters: RequestedPayload, navigation: str) -> Optional[DeclarativeMeta]:
    ins_filters = filters.nav_filters
    current_record = filters.loaded_record
    
    disposition = ins_filters.disposition
    factory_id = ins_filters.factory_id
    device_id = ins_filters.device_id
    job_id = ins_filters.job_id

    current_record_id = current_record.record_id
    current_factory_id = current_record.factory_id
    current_device_id = current_record.device_id
    
    current_range = []
    query = db.query(model)
    if factory_id != -1:
        query = query.filter(model.factory_id == factory_id)
    if device_id != -1:
        query = query.filter(model.device_id == device_id)
    if disposition != -1:
        query = query.filter(model.disposition == disposition)
    if job_id != -1:
        query = query.filter(model.job_id == job_id)

    current_range = query.order_by(model.timestamp.asc()).all()

    for idx, record in enumerate(current_range):
        if record.record_id == current_record_id and record.factory_id == current_factory_id and record.device_id == current_device_id:
            if navigation == "next" and idx + 1 < len(current_range):
                return current_range[idx + 1]
            elif navigation == "previous" and idx - 1 >= 0:
                return current_range[idx - 1]
            break
    
def get_factory_stats(db: Session, model: Type[DeclarativeMeta], factory_id: int) -> StatsData:
    result = (
        db.query(
            func.count().label("total_count"),
            func.sum(case((model.disposition == 1, 1), else_=0)).label("pass_count"),
            func.sum(case((model.disposition == 2, 1), else_=0)).label("fail_count"),
            func.sum(case((model.disposition == 3, 1), else_=0)).label("invalid_count")
        )
        .filter(model.factory_id == factory_id)
        .first()
    )

    factory_stats_data = StatsData(
        id=factory_id,
        total_count=result.total_count,
        pass_count=result.pass_count,
        fail_count=result.fail_count,
        invalid_count=result.invalid_count,
        pass_rate=(result.pass_count / result.total_count) * 100,
        fail_rate=(result.fail_count / result.total_count) * 100,
        invalid_rate=(result.invalid_count / result.total_count) * 100
    )
    return factory_stats_data

def get_device_stats(db: Session, model: Type[DeclarativeMeta], factory_id: int, device_id: int = -1) -> List[StatsData]:
    query = (
        db.query(
            model.device_id,
            func.count().label("total_count"),
            func.sum(case((model.disposition == 1, 1), else_=0)).label("pass_count"),
            func.sum(case((model.disposition == 2, 1), else_=0)).label("fail_count"),
            func.sum(case((model.disposition == 3, 1), else_=0)).label("invalid_count")
        )
        .filter(model.factory_id == factory_id)
    )
    if device_id != -1:
        query = query.filter(model.device_id == device_id)
    else:
        query = query.group_by(model.device_id)

    result = query.all()
    device_stats_data = []
    for row in result:
        device_stats_data.append(
            StatsData(
                id=row.device_id,
                total_count=row.total_count,
                pass_count=row.pass_count,
                fail_count=row.fail_count,
                invalid_count=row.invalid_count,
                pass_rate=(row.pass_count / row.total_count) * 100,
                fail_rate=(row.fail_count / row.total_count) * 100,
                invalid_rate=(row.invalid_count / row.total_count) * 100
            )
        )
    return device_stats_data

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