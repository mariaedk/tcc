"""
@author maria
date: 2025-02-25
"""
from sqlalchemy.orm import Session
from app.schemas.sensor_schema import SensorCreate, SensorResponse, SensorUpdate
from app.config import MessageLoader
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, DataError, InvalidRequestError, StatementError, DatabaseError
import app.repositories.sensor_repository as sensor_repository

class SensorService:

    @staticmethod
    def criar_sensor(db: Session, sensor_schema: SensorCreate) -> SensorResponse:
        if sensor_schema is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        sensor_dict = sensor_schema.model_dump()

        try:
            sensor = sensor_repository.save(db, sensor_dict)
        except DataError: # campo grande
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.tamanho_dados"))
        except InvalidRequestError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.requisicao_invalida"))
        except StatementError: # valor do enum inválido
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.valor_invalido"))
        except DatabaseError:
            db.rollback()
            raise HTTPException(status_code=500, detail=MessageLoader.get("erro.banco"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        sensor = SensorResponse.model_validate(sensor)
        return sensor

    @staticmethod
    def listar_sensores(db: Session):
        sensores = sensor_repository.find_all(db)
        return [SensorResponse.model_validate(sensor) for sensor in sensores]

    @staticmethod
    def buscar_sensor(db: Session, sensor_id: int):
        if sensor_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        sensor = sensor_repository.find_by_id(db, sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        return SensorResponse.model_validate(sensor)

    @staticmethod
    def excluir_sensor(db: Session, sensor_id: int):
        if sensor_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        sensor = sensor_repository.find_by_id(db, sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        try:
            sensor_repository.delete_by_id(db, sensor_id)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.dependencias"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        return True

    @staticmethod
    def atualizar_sensor(db: Session, sensor_schema: SensorUpdate) -> SensorResponse:
        sensor = sensor_repository.find_by_id(db, sensor_schema.id)
        if not sensor:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erros.sensor_nao_encontrado"))

        update_data = sensor_schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(sensor, key, value)

        db.commit()
        db.refresh(sensor)
        return SensorResponse.model_validate(sensor)