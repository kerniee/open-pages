from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl

from open_pages.files import get_files, get_sites
from open_pages.settings import SettingsDep
from open_pages.site import existing_site
from open_pages.ui.utils import get_site_from_referer

router = APIRouter(tags=["UI"])

templates = Jinja2Templates(directory="templates")


def get_site(referer: Annotated[HttpUrl | None, Header()] = None) -> str | None:
    if referer:
        return get_site_from_referer(referer)
    return None


SiteDep = Annotated[str | None, Depends(get_site)]


@router.get("/")
def index(request: Request, settings: SettingsDep) -> HTMLResponse:
    site_names = list(get_sites(settings))
    sites = {name: get_files(settings.data_dir / name) for name in site_names}
    return templates.TemplateResponse(
        request=request, name="index.html", context={"sites": sites}
    )


@router.get("/favicon.ico")
def favicon_ico() -> FileResponse:
    return FileResponse("templates/favicon.ico")


@router.get("/favicon-32x32.png")
def favicon_png() -> FileResponse:
    return FileResponse("templates/favicon-32x32.png")


@router.get("/{path:path}")
@router.get("/sites/{path:path}")
def visit_site(
    path: Path, settings: SettingsDep, site_from_referrer: SiteDep
) -> FileResponse:
    if site_from_referrer:
        site_name = site_from_referrer
        req_file_path = path
    else:
        site_name = str(path)
        req_file_path = Path("index.html")

    site_folder = existing_site(site_name, settings)

    headers = {"Cache-Control": "no-cache"}
    return FileResponse(site_folder / req_file_path, headers=headers)
