import asyncio
import os.path
import shutil
from pathlib import Path
from typing import Annotated, Awaitable

from fastapi import APIRouter, Depends, Form, UploadFile
from pydantic import BaseModel

from open_pages.common import AppException, log
from open_pages.files import get_files, save_file
from open_pages.settings import SettingsDep
from open_pages.site import SiteInfo, SiteName, get_existing_site, get_site_info

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/sites")
async def upload_site_files(
    files: list[UploadFile],
    settings: SettingsDep,
    name: Annotated[SiteName, Form(examples=[""])],
) -> str:
    site_folder = settings.data_dir / name
    site_folder.mkdir(exist_ok=True)

    prefix = ""
    if len(files) > 1:
        prefix = os.path.commonpath([file.filename for file in files if file.filename])
    log.debug(f"Prefix: {prefix}")

    tasks: list[Awaitable[None]] = []
    index_html_found = False
    for file in files:
        if not file.filename or file.filename == ".":
            await asyncio.gather(*tasks)
            shutil.rmtree(site_folder)
            raise AppException(f"Invalid file name: '{file.filename}'")
        relative_dst = Path(file.filename).relative_to(prefix)
        if relative_dst == Path("index.html"):
            index_html_found = True
        dst = site_folder / relative_dst
        tasks.append(save_file(file, dst, settings.chunk_size))

    await asyncio.gather(*tasks)

    if index_html_found is False:
        shutil.rmtree(site_folder)
        raise AppException("No index.html file found")

    return "ok"


@router.get("/sites/{site_name}/files")
def list_site_files(
    site_folder: Annotated[Path, Depends(get_existing_site)],
) -> list[str]:
    return sorted([file.name for file in get_files(site_folder)])


@router.get("/sites/{site_name}")
def get_site(site_folder: Annotated[Path, Depends(get_existing_site)]) -> SiteInfo:
    return get_site_info(site_folder)


@router.delete("/sites/{site_name}")
def delete_site(site_folder: Annotated[Path, Depends(get_existing_site)]) -> str:
    shutil.rmtree(site_folder)
    return "ok"


class ChangeSite(BaseModel):
    name: SiteName


@router.put("/sites/{site_name}")
def change_site(
    site_folder: Annotated[Path, Depends(get_existing_site)],
    changed_site: ChangeSite,
    settings: SettingsDep,
) -> str:
    try:
        existing_site = get_existing_site(changed_site.name, settings)
    except AppException:
        existing_site = None

    if existing_site is not None:
        raise AppException(f"Site with name '{changed_site.name}' already exists")

    site_folder.rename(site_folder.parent / changed_site.name)

    return "ok"
