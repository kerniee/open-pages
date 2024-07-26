import asyncio
import os.path
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile

from open_pages.common import AppException, log
from open_pages.files import get_files, save_file
from open_pages.settings import SettingsDep
from open_pages.site import SiteName, existing_site

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

    tasks = []
    for file in files:
        if not file.filename or file.filename == ".":
            raise AppException("Invalid file name")
        relative_dst = Path(file.filename).relative_to(prefix)
        dst = site_folder / relative_dst
        tasks.append(save_file(file, dst, settings.chunk_size))
    await asyncio.gather(*tasks)
    return "ok"


@router.get("/sites/{site_name}")
def list_site_files(site_folder: Annotated[Path, Depends(existing_site)]) -> list[str]:
    return [file.name for file in get_files(site_folder)]
