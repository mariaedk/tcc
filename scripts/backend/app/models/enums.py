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
