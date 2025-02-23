from fastapi import APIRouter

router = APIRouter()

@router.post("/medicoes/")
def criar_medicao():
    return { "msg": "Endpoint da medição criada" }
