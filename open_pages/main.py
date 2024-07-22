from fastapi import FastAPI

from open_pages.api.routes import router as api_router
from open_pages.ui.routes import router as ui_router

app = FastAPI()
app.include_router(api_router)
app.include_router(ui_router)
