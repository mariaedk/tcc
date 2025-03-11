from sqlalchemy import Column, BigInteger, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.enums import TipoSensor
import app.length_constants as length_constants


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_sensor")
    nome = Column(String(length_constants.SIZE_255), nullable=False, name="ds_nome")
    tipo = Column(Enum(TipoSensor, native_enum=False), nullable=False, name="tp_sensor")
    dispositivo_id = Column(BigInteger, ForeignKey("dispositivo.id_dispositivo"), nullable=False,
                            name="dispositivo_id_dispositivo")

    dispositivo = relationship("Dispositivo", backref="sensores")
