from app.database import SessionLocal
from app.models.usuario_model import Usuario
from app.models.dispositivo_model import Dispositivo
from app.models.sensor_model import Sensor
from app.models.unidade_medida_model import UnidadeMedida
from app.models.enums import TipoUsuario, TipoDispositivo, TipoSensor
from app.services.auth import hash_password

def seed():
    db = SessionLocal()
    try:
        if not db.query(Usuario).filter_by(username="admin").first():
            db.add(Usuario(
                nome="Administrador",
                username="admin",
                email="admin@tcc.local",
                senha=hash_password("admin123"),
                tipo=TipoUsuario.ADMIN,
            ))

        if not db.query(Usuario).filter_by(username="convidado").first():
            db.add(Usuario(
                nome="Convidado",
                username="convidado",
                email="convidado@tcc.local",
                senha=hash_password("pesquisa123"),
                tipo=TipoUsuario.COMUM,
            ))

        if not db.query(UnidadeMedida).filter_by(sigla="L/min").first():
            unidade = UnidadeMedida(denominacao="Litros por minuto", sigla="L/min")
            db.add(unidade)

        if not db.query(Dispositivo).filter_by(codigo=1).first():
            dispositivo = Dispositivo(
                nome="CLP ETA",
                codigo=1,
                tipo=TipoDispositivo.CLP,
                localizacao="Estação de Tratamento de Água",
            )
            db.add(dispositivo)
            db.flush()

            db.add(Sensor(nome="Vazão Saída 1", codigo=1, tipo=TipoSensor.VAZAO, dispositivo_id=dispositivo.id))
            db.add(Sensor(nome="Vazão Saída 2", codigo=2, tipo=TipoSensor.VAZAO, dispositivo_id=dispositivo.id))

        db.commit()
        print("Seed concluído.")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
