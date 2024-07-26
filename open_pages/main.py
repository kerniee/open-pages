from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from open_pages.api.routes import router as api_router
from open_pages.common import AppException
from open_pages.settings import SettingsDep
from open_pages.ui.routes import router as ui_router


def init_settings(settings: SettingsDep, req: Request) -> None:
    req.app.settings = settings


app = FastAPI(dependencies=[Depends(init_settings)])


@app.exception_handler(AppException)
async def unicorn_exception_handler(req: Request, exc: AppException) -> JSONResponse:
    if req.app.settings.catch_exceptions:
        return JSONResponse(
            status_code=400,
            content={"detail": exc.args[0]},
        )
    raise exc


app.include_router(api_router)
app.include_router(ui_router)
