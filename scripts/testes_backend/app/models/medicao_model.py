from sqlalchemy import Column, BigInteger, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base

class Medicao(Base):
    __tablename__ = "medicao"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_medicao")
    sensor_id = Column(BigInteger, ForeignKey("sensor.id_sensor"), nullable=False, name="sensor_id_sensor")
    unidade_id = Column(BigInteger, ForeignKey("unidade_medida.id_unidade_medida"), nullable=False, name="unidade_medida_id_unidade_medida")
    valor = Column(Float, nullable=False, name="vl_valor")
    data_hora = Column(DateTime, default=lambda: datetime.now(UTC), name="dt_hora")

    sensor = relationship("Sensor", backref="medicao")
    unidade = relationship("UnidadeMedida", backref="medicao")
