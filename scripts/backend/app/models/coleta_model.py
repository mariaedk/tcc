"""
@author maria
date: 2025-04-17
"""
from datetime import datetime, timezone
from sqlalchemy import Column, BigInteger, String, DateTime
from app.database import Base
from sqlalchemy.orm import relationship

UTC = timezone.utc

class Coleta(Base):
    __tablename__ = "coleta"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_coleta")
    data_hora = Column(DateTime, default=lambda: datetime.now(UTC), name="dt_hora")
    origem = Column(String(100), nullable=True)

    medicoes = relationship("Medicao", back_populates="coleta")
