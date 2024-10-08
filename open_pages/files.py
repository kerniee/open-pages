import os
from pathlib import Path
from typing import Iterable

import aiofiles
from fastapi import UploadFile

from open_pages.common import log
from open_pages.settings import SettingsDep


async def save_file(src: UploadFile, dst: Path, chunk_size: int) -> None:
    await src.seek(0)
    dst.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(dst, "wb") as buffer:
        while True:
            contents = await src.read(chunk_size)
            if not contents:
                log.debug("File saved")
                break
            log.debug(f"Read {src.filename}: {len(contents)} bytes")
            await buffer.write(contents)


def get_files(folder: Path) -> Iterable[Path]:
    assert folder.is_dir()
    for path, _, files in os.walk(folder):
        for name in files:
            yield Path(os.path.join(path, name))


def get_sites(settings: SettingsDep) -> Iterable[str]:
    for f in settings.data_dir.iterdir():
        if f.is_dir() and any(os.scandir(f)):
            yield f.name
