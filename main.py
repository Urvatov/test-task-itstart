from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Float, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date
from statistics import median

app = FastAPI()

Base = declarative_base()

class DeviceStat(Base):
    __tablename__ = "device_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    date = Column(Date)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@app.post("/users/")
def add_user():
    pass


@app.post("/stats/")
def add_stats(device_id: int, x: float, y: float, z: float, date : date):
    db = SessionLocal()
    stat = DeviceStat(device_id=device_id, x=x, y=y, z=z, date=date)
    db.add(stat)
    db.commit()
    db.close() 
    return {"message": f"Статистика для устройства {device_id} добавлена"}

@app.get("/stats/{device_id}")
def get_stats(device_id: int):
    db = SessionLocal()
    stats = db.query(DeviceStat).filter(DeviceStat.device_id == device_id).all()
    if not stats:
        raise HTTPException(status_code=404, detail=f"Статистика для устройства {device_id} не найдена")
    return stats

@app.get("/stats/analysis/")
def get_analysis(device_id: int, start_date: date = None, end_date: date = None):
    db = SessionLocal()
    query = db.query(DeviceStat).filter(DeviceStat.device_id == device_id)

    if start_date:
        query = query.filter(DeviceStat.date >= start_date)
    if end_date:
        query = query.filter(DeviceStat.date <= end_date)
    
    stats = query.all()
    if not stats:
        raise HTTPException(status_code=404, detail="Статистика не найдена")
    

    
    if start_date and end_date:
        time_interval = f"{str(start_date)} — {str(end_date)}"
    else:
        time_interval = "all_time"

    count = len(stats)
    X = [stat.x for stat in stats]
    min_x = min(X)
    max_x = max(X)
    sum_x = sum(X)
    mid_x = median(X)

    Y = [stat.y for stat in stats]
    min_y = min(Y)
    max_y = max(Y)
    sum_y = sum(Y)
    mid_y = median(Y)

    Z = [stat.z for stat in stats]
    min_z = min(Z)
    max_z = max(Z)
    sum_z = sum(Z)
    mid_z = median(Z)


    data = {
        "device_id" : device_id,
        "interval" : time_interval,
        "count": count,
        "min_x": min_x,
        "max_x": max_x,
        "sum_x": sum_x,
        "mid_x": mid_x,
        "min_y": min_y,
        "max_y": max_y,
        "sum_y": sum_y,
        "mid_y": mid_y,
        "min_z": min_z,
        "max_z": max_z,
        "sum_z": sum_z,
        "mid_z": mid_z
    }

    
    return { "data" : data }
