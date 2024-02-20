from fastapi import FastAPI, HTTPException
from datetime import date
from statistics import median
from models import User, Device, DeviceStat, SessionLocal

app = FastAPI()

@app.post("/users/")
def add_user(name : str):
    db = SessionLocal()
    user = User(name=name)
    db.add(user)
    db.commit()
    db.close() 

    return {"message" : f"Пользователь {name} добавлен"}


@app.post("/devices/")
def add_device(name : str, user_id : int = None):
    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователь {user_id} не найден")
    
    device = Device(name=name, user_id=user_id)
    db.add(device)
    db.commit()
    db.close() 

    return {"message" : f"Устройство {name} добавлено, пользователь: {user_id}"}


@app.post("/stats/")
def add_stats(device_id: int, x: float, y: float, z: float, date : date):
    db = SessionLocal()

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Устройство {device_id} не найдено")
    
    stat = DeviceStat(device_id=device_id, x=x, y=y, z=z, date=date)
    db.add(stat)
    db.commit()
    db.close() 
    return {"message": f"Статистика для устройства {device_id} добавлена"}

@app.get("/stats/{device_id}")
def get_stats_by_device(device_id: int):
    db = SessionLocal()
    stats = db.query(DeviceStat).filter(DeviceStat.device_id == device_id).all()
    if not stats:
        raise HTTPException(status_code=404, detail=f"Статистика для устройства {device_id} не найдена")
    return stats

@app.get("/stats/analysis/")
def get_analysis_by_device(device_id: int, start_date: date = None, end_date: date = None):
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

@app.get("/users/analysis")
def get_analysis_by_user(user_id: int, device_id: int = None):
    db = SessionLocal()

    if device_id:
        devices = db.query(Device).filter(Device.user_id == user_id, Device.id == device_id).all()
    else:
        devices = db.query(Device).filter(Device.user_id == user_id).all()
        print(devices)

    if not devices:
        raise HTTPException(status_code=404, detail=f"Устройства пользователя {user_id} не найдены")

    result = {}
    for device in devices:
        print(device)
        stats_query = db.query(DeviceStat).filter(DeviceStat.device_id == device.id)
        stats = stats_query.all()

        if not stats:
            continue  

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
            "device_id": device.id,
            "device_name": device.name,
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

       
        result[device.id] = data
    return {"data": result}
