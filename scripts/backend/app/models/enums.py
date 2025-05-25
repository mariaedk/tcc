from enum import Enum

class TipoUsuario(str, Enum):
    ADMIN = "ADMIN"
    COMUM = "COMUM"

class TipoDispositivo(str, Enum):
    RASPBERRY = "RASPBERRY"
    CLP = "CLP"

class TipoSensor(str, Enum):
    TEMPERATURA = "TEMPERATURA"
    VAZAO = "VAZAO"
    PRESSAO = "PRESSAO"
    NIVEL = "NIVEL"

class TipoMedicao(str, Enum):
    HORA = "HORA"
    DIA = "DIA"
    INST = "INST"
