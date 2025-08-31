from json import dumps

from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from structlog.contextvars import bind_contextvars
from structlog.stdlib import BoundLogger, get_logger

from backend.schemas.email import EmailIn, EmailList, EmailModel
from backend.utils.deps import AMQPQueueDep, DatabaseDep

logger: BoundLogger = get_logger()
router = APIRouter(prefix="/email")


@router.post("")
@router.post("/")
async def post_index(db: DatabaseDep, queue: AMQPQueueDep, email_in: EmailIn) -> JSONResponse:
    email = await db.put_item("email", EmailModel.from_email_in(email_in))

    await queue.send(dumps(email).encode())
    return JSONResponse({"status": "Success", "data": email}, 201)


@router.get("/page")
async def get_index(db: DatabaseDep, body: EmailList) -> JSONResponse:
    page = await db.get_page(body.page)
    return JSONResponse({"status": "Success", "data": page}, 200)


@router.get("/pages")
async def get_pages(db: DatabaseDep) -> JSONResponse:
    total_pages = await db.get_total_pages()
    return JSONResponse({"status": "Success", "data": total_pages}, 200)


@router.get("/{email_id}")
async def get_email(email_id: str, db: DatabaseDep) -> JSONResponse:
    bind_contextvars(email_id=email_id)

    try:
        email = await db.get_item("email", email_id)
        return JSONResponse({"status": "Success", "data": email})
    except ValueError:
        logger.info("content not found")
        return JSONResponse({"status": "Failed", "message": "content not found."}, 404)
