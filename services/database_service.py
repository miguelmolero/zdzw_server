# services/generic_service.py
from sqlalchemy.orm import Session
from typing import Type, List, Optional
from sqlalchemy.ext.declarative import DeclarativeMeta
from database.database import Base

# Select by ID
def SelectById(db: Session, model: Type[DeclarativeMeta], instance_id: int):
    return db.query(model).filter(model.id == instance_id).first()

# Select all rows of a table
def SelectAll(db: Session, model: Type[DeclarativeMeta]) -> List[DeclarativeMeta]:
    return db.query(model).all()

# Insert a new row
def Insert(db: Session, model: Type[DeclarativeMeta], **kwargs) -> DeclarativeMeta:
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
    return instance

# Update an existing row
def Update(db: Session, model: Type[DeclarativeMeta], instance_id: int, **kwargs) -> Optional[DeclarativeMeta]:
    instance = db.query(model).filter(model.id == instance_id).first()
    if not instance:
        return None
    for key, value in kwargs.items():
        setattr(instance, key, value)
    db.commit()
    db.refresh(instance)
    return instance

# Delete an existing row
def Delete(db: Session, model: Type[DeclarativeMeta], instance_id: int) -> Optional[DeclarativeMeta]:
    instance = db.query(model).filter(model.id == instance_id).first()
    if instance:
        db.delete(instance)
        db.commit()
    return instance
