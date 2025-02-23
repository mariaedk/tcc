from fastapi import APIRouter
from .medicao import router as medicao_router
from .usuario import router as usuario_router

router = APIRouter()
router.include_router(medicao_router)
router.include_router(usuario_router)
