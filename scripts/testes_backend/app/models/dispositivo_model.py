from sqlalchemy import Column, BigInteger, String, Enum
from app.database import Base
from app.models.enums import TipoDispositivo
import app.length_constants as length_constants

class Dispositivo(Base):
    __tablename__ = "dispositivo"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_dispositivo")
    nome = Column(String(length_constants.SIZE_255), nullable=False, name="ds_nome")
    tipo = Column(Enum(TipoDispositivo, native_enum=False), nullable=False, name="tp_dispositivo")
    localizacao = Column(String(length_constants.SIZE_255), nullable=True, name="ds_localizacao")
