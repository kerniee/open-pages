import asyncio
import logging
from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import Depends, FastAPI, UploadFile
from pydantic import StringConstraints

from open_pages.settings import Settings, get_settings

log = logging.getLogger(__name__)
app = FastAPI()
FileName = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_\-\.]+$")]
SettingsDep = Annotated[Settings, Depends(get_settings)]


async def save_file(src: UploadFile, dst: Path, chunk_size: int):
    await src.seek(0)
    async with aiofiles.open(dst, "wb") as buffer:
        while True:
            contents = await src.read(chunk_size)
            if not contents:
                log.debug("File saved")
                break
            log.debug(f"Read {src.filename}: {len(contents)} bytes")
            await buffer.write(contents)


@app.post("/sites/{name}")
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


@app.get("/sites/{name}", response_model=list[str])
async def list_site_files(name: FileName, settings: SettingsDep):
    site_folder = settings.data_dir / name
    return [file.name for file in site_folder.iterdir() if file.is_file()]
