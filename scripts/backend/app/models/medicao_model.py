from sqlalchemy import Column, BigInteger, Float, ForeignKey, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base
UTC = timezone.utc

class Medicao(Base):
    __tablename__ = "medicao"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_medicao")

    coleta_id = Column(BigInteger, ForeignKey("coleta.id_coleta"), nullable=False, name="coleta_id_coleta")
    sensor_id = Column(BigInteger, ForeignKey("sensor.id_sensor"), nullable=False, name="sensor_id_sensor")
    unidade_id = Column(BigInteger, ForeignKey("unidade_medida.id_unidade_medida"), nullable=False, name="unidade_medida_id_unidade_medida")

    valor = Column(Float, nullable=True, name="vl_valor")
    valor_str = Column(String(255), nullable=True, name="vl_valor_str")
    valor_bool = Column(Boolean, nullable=True, name="vl_valor_bool")

    data_hora = Column(DateTime, default=lambda: datetime.now(UTC), name="dt_hora")

    coleta = relationship("Coleta", back_populates="medicoes")
    sensor = relationship("Sensor", backref="medicao")
    unidade = relationship("UnidadeMedida", backref="medicao")
