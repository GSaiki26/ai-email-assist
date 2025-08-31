from fastapi import FastAPI
from fastapi.responses import JSONResponse
from structlog import get_logger
from structlog.stdlib import BoundLogger

from backend.middlewares.logger import set_logger
from backend.routes.email import router as email_router
from backend.settings import Settings

logger: BoundLogger = get_logger()
settings = Settings()


app = FastAPI()
app.middleware("http")(set_logger)
app.include_router(email_router)


@app.route("/{full_path:path}")
def default_route(_path: str) -> JSONResponse:
    return JSONResponse({"status": "Failed", "message": "Route not found"}, 404)
