from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from open_pages.files import get_files, get_sites
from open_pages.settings import SettingsDep

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, settings: SettingsDep) -> HTMLResponse:
    site_names = list(get_sites(settings))
    sites = {name: get_files(name, settings) for name in site_names}
    return templates.TemplateResponse(
        request=request, name="index.html", context={"sites": sites}
    )
