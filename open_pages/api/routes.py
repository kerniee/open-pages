import asyncio
from typing import Annotated

from fastapi import APIRouter, UploadFile
from pydantic import StringConstraints

from open_pages.common import AppException
from open_pages.files import get_files, save_file
from open_pages.settings import SettingsDep

router = APIRouter(prefix="/api")

FileName = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_\-]+$")]


@router.post("/sites/{name}")
async def upload_site_files(
    files: list[UploadFile], name: FileName, settings: SettingsDep
) -> str:
    site_folder = settings.data_dir / name
    site_folder.mkdir(exist_ok=True)

    tasks = []
    for file in files:
        if not file.filename:
            raise AppException("Invalid file name")
        dst = site_folder / file.filename
        tasks.append(save_file(file, dst, settings.chunk_size))
    await asyncio.gather(*tasks)
    return "ok"


@router.get("/sites/{site_name}")
def list_site_files(site_name: FileName, settings: SettingsDep) -> list[str]:
    return [file.name for file in get_files(site_name, settings)]
