import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.opc_ua.reader import loop_opc_ua
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(loop_opc_ua())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)

# configuração de CORS
origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://127.0.0.1",
    "http://127.0.0.1:4200",
    "http://54.207.122.55",
    "http://maria-tcc-monitoramento-ambiental.duckdns.org"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def home():
    return {"msg": "api do TCC"}
