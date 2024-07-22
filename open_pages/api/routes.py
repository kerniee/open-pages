import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from pydantic import StringConstraints

from open_pages.api.files import save_file
from open_pages.settings import Settings, get_settings

router = APIRouter(prefix="/api")

FileName = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_\-\.]+$")]
SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.post("/sites/{name}")
async def upload_site_files(
    files: list[UploadFile], name: FileName, settings: SettingsDep
):
    site_folder = settings.data_dir / name
    site_folder.mkdir(exist_ok=True)

    tasks = []
    for file in files:
        if not file.filename:
            raise ValueError("Invalid file name")
        dst = site_folder / file.filename
        tasks.append(save_file(file, dst, 1024))
    await asyncio.gather(*tasks)
    return "ok"


@router.get("/sites/{name}", response_model=list[str])
async def list_site_files(name: FileName, settings: SettingsDep):
    site_folder = settings.data_dir / name
    return [file.name for file in site_folder.iterdir() if file.is_file()]
