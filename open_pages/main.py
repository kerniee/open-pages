from typing import Any, Callable, Coroutine

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse

from open_pages.api.routes import router as api_router
from open_pages.common import AppException
from open_pages.settings import SettingsDep
from open_pages.ui.routes import router as ui_router


def init_settings(settings: SettingsDep, req: Request) -> None:
    req.app.settings = settings


app = FastAPI(dependencies=[Depends(init_settings)])
MiddlewareCallable = Callable[..., Coroutine[Any, Any, Response]]


@app.exception_handler(AppException)
async def unicorn_exception_handler(req: Request, exc: AppException) -> JSONResponse:
    if req.app.settings.catch_exceptions:
        return JSONResponse(
            status_code=400,
            content={"detail": exc.args[0]},
        )
    raise exc


@app.middleware("http")
async def add_referrer_header(req: Request, call_next: MiddlewareCallable) -> Response:
    resp = await call_next(req)
    resp.headers["Referrer-Policy"] = "same-origin"
    return resp


app.include_router(api_router)
app.include_router(ui_router)
