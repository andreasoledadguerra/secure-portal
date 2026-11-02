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