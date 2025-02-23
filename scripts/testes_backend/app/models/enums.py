import enum

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
