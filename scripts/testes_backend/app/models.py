import app.length_constants as length_constants
import enum
from sqlalchemy import Column, BigInteger, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, UTC

# Enums
class TipoUsuario(enum.Enum):
    ADMIN = 0
    COMUM = 1

class TipoDispositivo(enum.Enum):
    RASPBERRY = 0
    CLP = 1

class TipoSensor(enum.Enum):
    TEMPERATURA = 0
    VAZAO = 1
    PRESSAO = 2

# Models
class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_usuario")
    nome = Column(String(length_constants.SIZE_255), nullable=False, name="ds_nome")
    username = Column(String(length_constants.SIZE_100), nullable=False, unique=True, name="ds_username")
    email = Column(String(length_constants.SIZE_255), nullable=False, unique=True, name="ds_email")
    senha = Column(String(length_constants.SIZE_400), nullable=False, name="ds_senha")
    tipo = Column(Enum(TipoUsuario, native_enum=False), nullable=False, name="tp_usuario")

class Dispositivo(Base):
    __tablename__ = "dispositivo"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_dispositivo")
    nome = Column(String(length_constants.SIZE_255), nullable=False, name="ds_nome")
    tipo = Column(Enum(TipoDispositivo, native_enum=False), nullable=False, name="tp_dispositivo")
    localizacao = Column(String(length_constants.SIZE_255), nullable=True, name="ds_localizacao")

class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_sensor")
    nome = Column(String(length_constants.SIZE_255), nullable=False, name="ds_nome")
    tipo = Column(Enum(TipoSensor, native_enum=False), nullable=False, name="tp_sensor")
    dispositivo_id = Column(BigInteger, ForeignKey("dispositivo.id_dispositivo"), nullable=False, name="dispositivo_id_dispositivo")
    dispositivo = relationship("Dispositivo", backref="sensores")

class UnidadeMedida(Base):
    __tablename__ = "unidade_medida"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_unidade_medida")
    denominacao = Column(String(length_constants.SIZE_50), nullable=False, name="ds_denominacao")
    sigla = Column(String(length_constants.SIZE_10), nullable=False, name="ds_sigla")

class Medicao(Base):
    __tablename__ = "medicao"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_medicao")
    sensor_id = Column(BigInteger, ForeignKey("sensor.id_sensor"), nullable=False, name="sensor_id_sensor")
    unidade_id = Column(BigInteger, ForeignKey("unidade_medida.id_unidade_medida"), nullable=False, name="unidade_medida_id_unidade_medida")
    valor = Column(Float, nullable=False, name="vl_valor")
    data_hora = Column(DateTime, default=lambda: datetime.now(UTC), name="dt_hora")

    sensor = relationship("Sensor", backref="medicao")
    unidade = relationship("UnidadeMedida", backref="medicao")