from sqlalchemy import create_engine, Column, Float, String, Date, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    devices = relationship("Device", back_populates="user")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    name = Column(String)

    user = relationship("User", back_populates="devices")

class DeviceStat(Base):
    __tablename__ = "device_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    date = Column(Date)
