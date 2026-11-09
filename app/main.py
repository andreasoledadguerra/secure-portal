from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import auth, users
from app.core.database import engine, Base
from app.core.config import settings
from app.core.listeners import auth_event_listener



@asynccontextmanager
async def lifespan(app: FastAPI):
    #async with engine.begin() as conn:
    await auth_event_listener.start()  # Inicia el listener de eventos de autenticación
    yield
    await auth_event_listener.stop()  # Detiene el listener de eventos de autenticación
    await engine.dispose()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

#app.mount("/static", StaticFiles(directory="app/static"), name="static")
#
#@app.get("/")
#async def root():
#    return FileResponse("app/static/index.html")
