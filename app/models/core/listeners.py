import asyncio
import json
import logging
from typing import Optional
import asyncpg
from app.core.config import settings    


logger = logging.getLogger("svp.listeners")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    logger.addHandler(handler)


class AuthEventListener:
    """
    Mantiene una conexión dedicada a PostgreSQL para escuchar 'auth_events'.
    No interfiere con el pool de SQLAlchemy: usa asyncpg directamente.
    """

    def __init__(self):
        self._conn: Optional[asyncpg.Connection] = None
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def _on_notify(self, connection, pid, channel, payload):
        """Callback ejecutado cada vez que llega una NOTIFY."""
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            logger.warning("Payload no JSON en canal %s: %s", channel, payload)
            return

        event_type = data.get("event")
        email = data.get("email")
        logger.info("Auth event recibido: %s | email=%s | payload=%s", event_type, email, data)

        # Aquí podrías reenviar a un ConnectionManager WebSocket:
        # from app.services.ws_manager import ws_manager
        # await ws_manager.broadcast(payload)

    async def start(self):
        """Abre la conexión, ejecuta LISTEN y queda escuchando."""
        if self._running:
            return

        # asyncpg requiere una URL sin el prefijo '+asyncpg'
        dsn = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

        try:
            self._conn = await asyncpg.connect(dsn)
            await self._conn.add_listener("auth_events", self._on_notify)
            self._running = True
            logger.info("Listener iniciado en canal 'auth_events' (PID=%s)", self._conn.get_server_pid())
        except Exception as e:
            logger.exception("No se pudo iniciar el listener: %s", e)
            raise

    async def stop(self):
        """Cierra la conexión limpiamente."""
        if not self._running or self._conn is None:
            return
        try:
            await self._conn.remove_listener("auth_events", self._on_notify)
            await self._conn.close()
            logger.info("Listener detenido correctamente.")
        except Exception as e:
            logger.warning("Error al detener el listener: %s", e)
        finally:
            self._running = False
            self._conn = None
