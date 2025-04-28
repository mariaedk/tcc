"""
@author maria
date: 2025-02-27
"""
from typing import Optional

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
    def buscar_por_data(db: Session, data: datetime):
        if not data:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        medicoes = medicao_repository.buscar_por_data_inicio(db, data)

        return [
            MedicaoHistoricoSchema(data=r.data, valor=round(r.media_valor, 2))
            for r in medicoes
        ]

    @staticmethod
    def buscar_por_intervalo_datas(db: Session, data_inicio: datetime, data_fim: datetime):
        if not data_inicio or not data_fim:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

        medicoes = medicao_repository.buscar_por_intervalo_datas(db, data_inicio, data_fim)

        return [
            MedicaoHistoricoSchema(data=r.data, valor=round(r.media_valor, 2))
            for r in medicoes
        ]

    @staticmethod
    def comparar_vazoes_por_mes(
        db: Session,
        codigo_entrada: int,
        codigo_saida: int,
        meses: Optional[int] = 6,
        data_inicio: Optional[datetime] = None,
        data_fim: Optional[datetime] = None
    ) -> ComparativoVazaoResponseSchema:
        resultados = medicao_repository.comparar_vazoes_por_mes(
            db,
            codigo_entrada,
            codigo_saida,
            meses,
            data_inicio,
            data_fim
        )

        resultado = {}
        for linha in resultados:
            mes = linha.mes
            if mes not in resultado:
                resultado[mes] = {"entrada": 0, "saida": 0}
            if linha.codigo_sensor == codigo_entrada:
                resultado[mes]["entrada"] = float(round(linha.media_valor, 2))
            elif linha.codigo_sensor == codigo_saida:
                resultado[mes]["saida"] = float(round(linha.media_valor, 2))

        # Prepara o schema de resposta
        categorias = list(resultado.keys())
        entrada = [resultado[m]["entrada"] for m in categorias]
        saida = [resultado[m]["saida"] for m in categorias]

        return ComparativoVazaoResponseSchema(
            categorias=categorias,
            series=[
                SerieComparativaSchema(name="Vazão de Entrada", data=entrada),
                SerieComparativaSchema(name="Vazão de Saída", data=saida)
            ]
        )

    @staticmethod
    def buscar_medicoes_geral(db: Session, sensor_codigo: int, data: datetime = None, data_inicio: datetime = None,
                              data_fim: datetime = None, dias: int = None) -> list[MedicaoHistoricoSchema]:
        medicoes = medicao_repository.buscar_medicoes_geral(db, sensor_codigo, data, data_inicio, data_fim, dias)
        return [MedicaoHistoricoSchema(data=medicao.data_hora.date(), valor=medicao.valor) for medicao in medicoes]

    @staticmethod
    def buscar_medicoes_media_por_dia(db: Session, sensor_codigo: int, data: datetime = None,
                                      data_inicio: datetime = None, data_fim: datetime = None,
                                      dias: int = None) -> list[MedicaoHistoricoSchema]:
        if not sensor_codigo:
            raise HTTPException(status_code=400, detail=MessageLoader.get("erro.sensor_nao_encontrado"))

        resultados = medicao_repository.buscar_medicoes_media_por_dia(db, sensor_codigo, data, data_inicio, data_fim, dias)

        return [
            MedicaoHistoricoSchema(data=r.data, valor=round(r.media_valor, 2))
            for r in resultados
        ]


