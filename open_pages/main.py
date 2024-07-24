from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from open_pages.api.routes import router as api_router
from open_pages.common import AppException
from open_pages.ui.routes import router as ui_router

app = FastAPI()


@app.exception_handler(AppException)
async def unicorn_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"message": exc.args[0]},
    )


app.include_router(api_router)
app.include_router(ui_router)
