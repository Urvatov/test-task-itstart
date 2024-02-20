from fastapi import FastAPI, HTTPException
from datetime import date
from statistics import median
from models import User, Device, DeviceStat, SessionLocal
from schemas import DeviceInput, UserInput, DeviceStatInput

app = FastAPI()


@app.post("/users/")
def add_user(data : UserInput):
    db = SessionLocal()
    user = User(name=data.name)
    db.add(user)
    db.commit()
    db.close() 

    return {"message" : f"Пользователь {data.name} добавлен"}


@app.post("/devices/")
def add_device(data : DeviceInput):
    db = SessionLocal()

    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Пользователь {data.user_id} не найден")
    
    device = Device(name=data.name, user_id=data.user_id)
    db.add(device)
    db.commit()
    db.close() 

    return {"message" : f"Устройство {data.name} добавлено, пользователь: {data.user_id}"}


@app.post("/stats/")
def add_stats(data: DeviceStatInput):
    db = SessionLocal() 

    device = db.query(Device).filter(Device.id == data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Устройство {data.device_id} не найдено")
    
    stat = DeviceStat(device_id=data.device_id, x=data.x, y=data.y, z=data.z, date=data.date)
    db.add(stat)
    db.commit()
    db.close() 
    return {"message": f"Статистика для устройства {data.device_id} добавлена"}

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
    
    return data

@app.get("/users/analysis")
def get_analysis_by_user(user_id: int, device_id: int = None):
    db = SessionLocal()

    if device_id:
        devices = db.query(Device).filter(Device.user_id == user_id, Device.id == device_id).all()
    else:
        devices = db.query(Device).filter(Device.user_id == user_id).all()

    if not devices:
        raise HTTPException(status_code=404, detail=f"Устройства пользователя {user_id} не найдены")

    result = {}
    for device in devices:
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
