from pydantic import BaseModel
from datetime import date

class DeviceStatInput(BaseModel):
    device_id : int
    x : float
    y : float
    z : float
    date : date

class UserInput(BaseModel):
    name : str
    
    

class DeviceInput(BaseModel):
    name : str
    user_id : int