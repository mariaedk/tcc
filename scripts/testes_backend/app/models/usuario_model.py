from sqlalchemy import Column, BigInteger, String, Enum
from app.database import Base
from app.models.enums import TipoUsuario
import app.length_constants as length_constants

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_usuario")
    nome = Column(String(length_constants.SIZE_255), nullable=False, name="ds_nome")
    username = Column(String(length_constants.SIZE_100), nullable=False, unique=True, name="ds_username")
    email = Column(String(length_constants.SIZE_255), nullable=False, unique=True, name="ds_email")
    senha = Column(String(length_constants.SIZE_400), nullable=False, name="ds_senha")
    tipo = Column(Enum(TipoUsuario, native_enum=False), nullable=False, name="tp_usuario")
