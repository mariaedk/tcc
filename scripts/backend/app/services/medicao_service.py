"""
@author maria
date: 2025-02-27
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.medicao_schema import MedicaoCreate, MedicaoResponse, MedicaoHistoricoSchema, ComparativoVazaoResponseSchema, SerieComparativaSchema
from app.repositories.medicao_repository import MedicaoRepository as medicao_repository
from app.config import MessageLoader
from sqlalchemy.exc import InvalidRequestError, DatabaseError
from app.models.medicao_model import Medicao
from datetime import datetime

class MedicaoService:

    @staticmethod
    def criar_medicao(db: Session, medicao_schema: MedicaoCreate) -> MedicaoResponse:
        if medicao_schema is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        medicao_dict = medicao_schema.model_dump()
        medicao_obj = Medicao(**medicao_dict)

        try:
            medicao = medicao_repository.save(db, medicao_obj)
        except InvalidRequestError:
            db.rollback()
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.requisicao_invalida"))
        except DatabaseError:
            db.rollback()
            raise HTTPException(status_code=500, detail=MessageLoader.get("erro.banco"))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")

        return MedicaoResponse.model_validate(medicao)

    @staticmethod
    def listar_medicoes(db: Session):
        medicoes = medicao_repository.find_all(db)
        return [MedicaoResponse.model_validate(medicao) for medicao in medicoes]

    @staticmethod
    def listar_medicoes_paginadas(db: Session, limit: int = 10, offset: int = 0):
        medicoes = medicao_repository.find_all_paginate(db, limit, offset)
        return [MedicaoResponse.model_validate(medicao) for medicao in medicoes]

    @staticmethod
    def buscar_medicao(db: Session, medicao_id: int):
        if medicao_id is None:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        medicao = medicao_repository.find_by_id(db, medicao_id)
        if not medicao:
            raise HTTPException(status_code=404, detail=MessageLoader.get("erro.medicao_nao_encontrada"))

        return MedicaoResponse.model_validate(medicao)

    @staticmethod
    def obter_historico_por_sensor(db: Session, cd_sensor: int, dias: int = 30) -> list[MedicaoHistoricoSchema]:
        if not cd_sensor:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        resultados = medicao_repository.media_por_dia_por_sensor(db, cd_sensor, dias)

        return [
            MedicaoHistoricoSchema(data=r.data, valor=round(r.media_valor, 2))
            for r in resultados
        ]

    @staticmethod
    def obter_historico_por_dispositivo(db: Session, cd_dispositivo: int, dias: int = 30) -> list[MedicaoHistoricoSchema]:
        if not cd_dispositivo:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        resultados = medicao_repository.media_por_dia_por_dispositivo(db, cd_dispositivo, dias)

        return [
            MedicaoHistoricoSchema(data=r.data, valor=round(r.media_valor, 2))
            for r in resultados
        ]

    @staticmethod
    def buscar_por_sensor(db: Session, sensor_id: int):
        medicoes = medicao_repository.buscar_por_sensor(db, sensor_id)
        return [MedicaoResponse.model_validate(m) for m in medicoes]

    @staticmethod
    def buscar_por_coleta(db: Session, coleta_id: int):
        medicoes = medicao_repository.buscar_por_coleta(db, coleta_id)
        return [MedicaoResponse.model_validate(m) for m in medicoes]

    @staticmethod
    def buscar_por_unidade(db: Session, unidade_id: int):
        medicoes = medicao_repository.buscar_por_unidade(db, unidade_id)
        return [MedicaoResponse.model_validate(m) for m in medicoes]

    @staticmethod
    def buscar_por_data_inicio(db: Session, data_inicio: datetime):
        medicoes = medicao_repository.buscar_por_data_inicio(db, data_inicio)
        return [MedicaoResponse.model_validate(m) for m in medicoes]

    @staticmethod
    def buscar_por_data_fim(db: Session, data_fim: datetime):
        medicoes = medicao_repository.buscar_por_data_fim(db, data_fim)
        return [MedicaoResponse.model_validate(m) for m in medicoes]

    @staticmethod
    def buscar_por_intervalo_datas(db: Session, data_inicio: datetime, data_fim: datetime):
        medicoes = medicao_repository.buscar_por_intervalo_datas(db, data_inicio, data_fim)
        return [MedicaoResponse.model_validate(m) for m in medicoes]

    @staticmethod
    def comparar_vazoes_por_dia(db: Session, codigo_entrada: int, codigo_saida: int, dias: int = 7) -> ComparativoVazaoResponseSchema:
        if not codigo_entrada or not codigo_saida:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        resultados = medicao_repository.comparar_vazoes_por_dia(db, codigo_entrada, codigo_saida, dias)

        resultado = {}
        for linha in resultados:
            data = linha.data.strftime('%d/%m')
            if data not in resultado:
                resultado[data] = {"entrada": 0, "saida": 0}
            if linha.codigo_sensor == codigo_entrada:
                resultado[data]["entrada"] = linha.media_valor
            elif linha.codigo_sensor == codigo_saida:
                resultado[data]["saida"] = linha.media_valor

        categorias = list(resultado.keys())
        entrada = [resultado[d]["entrada"] for d in categorias]
        saida = [resultado[d]["saida"] for d in categorias]

        return ComparativoVazaoResponseSchema(
            categorias=categorias,
            series=[
                SerieComparativaSchema(name="Vazão de Entrada", data=entrada),
                SerieComparativaSchema(name="Vazão de Saída", data=saida),
            ]
        )
