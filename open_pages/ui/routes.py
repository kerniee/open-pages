from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl

from open_pages.files import get_files, get_sites
from open_pages.settings import SettingsDep
from open_pages.site import existing_site, get_site_info
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
    sites = []
    for name in get_sites(settings):
        path = settings.data_dir / name
        sites.append(
            {
                "name": name,
                "files": get_files(path),
                "info": get_site_info(path),
            }
        )
    sites.sort(key=lambda x: x["info"].last_modified, reverse=True)  # type: ignore
    return templates.TemplateResponse(
        request=request, name="index.jinja", context={"sites": sites}
    )


@router.get("/favicon.ico")
def favicon_ico() -> FileResponse:
    return FileResponse("templates/favicon.ico")


@router.get("/favicon-32x32.png")
def favicon_png() -> FileResponse:
    return FileResponse("templates/favicon-32x32.png")


@router.get("/static/{path:path}")
def uikit(path: Path) -> FileResponse:
    return FileResponse(f"templates/static/{path}")


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
