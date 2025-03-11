from sqlalchemy import Column, BigInteger, String
from app.database import Base
import app.length_constants as length_constants

class UnidadeMedida(Base):
    __tablename__ = "unidade_medida"

    id = Column(BigInteger, primary_key=True, autoincrement=True, name="id_unidade_medida")
    denominacao = Column(String(length_constants.SIZE_50), nullable=False, name="ds_denominacao")
    sigla = Column(String(length_constants.SIZE_10), nullable=False, name="ds_sigla")
