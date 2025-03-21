# db/database.py
import os
from pathlib import Path
from database.database_conection import SessionLocal, engine, Base
from utils.security import hash_password
from database.models.Users.users import User



# initialize the database
def init_db():
    if not Path("./zdzw.db").exists():
        print("Database not found, creating...")
    Base.metadata.create_all(bind=engine)  # Crea las tablas si no existen
    db = SessionLocal()
    try:
        print("Adding default users")
        innerspec_user = db.query(User).filter(User.user == 'innerspec').first()
        if not innerspec_user:
            new_user = User(
                user="innerspec", 
                password=hash_password("innerspec!root#1"),
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        admin_user = db.query(User).filter(User.user == 'admin').first()
        if not admin_user:
            new_user = User(
                user="admin", 
                password=hash_password("admin123"),
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
    except Exception as e:
        print(e)
    finally:
        db.close()




