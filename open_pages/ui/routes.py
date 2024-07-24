from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from open_pages.files import get_files, get_sites
from open_pages.settings import SettingsDep

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request, settings: SettingsDep) -> HTMLResponse:
    site_names = list(get_sites(settings))
    sites = {name: get_files(name, settings) for name in site_names}
    return templates.TemplateResponse(
        request=request, name="index.html", context={"sites": sites}
    )


@router.get("/sites/{site_name}", response_class=HTMLResponse)
def visit_site(site_name: str, settings: SettingsDep) -> HTMLResponse:
    files = list(get_files(site_name, settings))

    chosen_file = None
    for file in files:
        if file.name == "index.html":
            chosen_file = file
            break
    if not chosen_file:
        raise ValueError("No index.html found")

    with open(chosen_file) as f:
        content = f.read()
        return HTMLResponse(content=content)
