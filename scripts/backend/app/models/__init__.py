# faz com que o Base.metadata.create_all() reconheça todos os modelos corretamente
# e expoe os imports
from app.database import Base
from app.models.usuario_model import Usuario
from app.models.dispositivo_model import Dispositivo
from app.models.sensor_model import Sensor
from app.models.unidade_medida_model import UnidadeMedida
from app.models.medicao_model import Medicao
from app.models.coleta_model import Coleta
