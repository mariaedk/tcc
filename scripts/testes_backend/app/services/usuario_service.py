from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate

def criar_usuario(db: Session, usuario: UsuarioCreate):
    novo_usuario = Usuario(**usuario.dict())
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario
