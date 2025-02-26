"""
@author maria
date: 2025-02-25
"""
from sqlalchemy.orm import Session
from app.models.sensor_model import Sensor

class SensorRepository:

    @staticmethod
    def find_all(db: Session) -> list[Sensor]:
        return db.query(Sensor).all()

    @staticmethod
    def find_all_paginate(db: Session, limit: int = 10, offset: int = 0):
        return db.query(Sensor).offset(offset).limit(limit).all()

    @staticmethod
    def save(db: Session, sensor: Sensor) -> Sensor:
        if sensor.id:
            db.merge(sensor)
        else:
            db.add(sensor)
        db.commit()
        db.refresh(sensor)
        return sensor

    @staticmethod
    def find_by_id(db: Session, id: int) -> Sensor | None:
        return db.query(Sensor).filter(Sensor.id == id).first()

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        sensor = db.query(Sensor).filter(Sensor.id == id).first()
        if sensor:
            db.delete(sensor)
            db.commit()