"""
@author maria
date: 2025-03-16
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.services.auth import verify_password, create_access_token
from app.services.usuario_service import UsuarioService
from app.database import SessionLocal
from datetime import timedelta
from app.config import MessageLoader

usuario_service = UsuarioService()
auth_router = APIRouter(prefix="/auth", tags=["Autenticação"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    if not form_data:
        raise HTTPException(status_code=400, detail=MessageLoader.get("erro.parametro_nao_informado"))

    usuario = usuario_service.buscar_usuario_por_nome(db, form_data.username)

    if not usuario or not verify_password(form_data.password, usuario.senha):
        raise HTTPException(status_code=400, detail=MessageLoader.get("erro.usuario_nao_encontrado"))

    token = create_access_token({"sub": usuario.username}, timedelta(minutes=60))
    return {"access_token": token, "token_type": "bearer"}
