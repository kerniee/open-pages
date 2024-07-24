from pathlib import Path
from typing import Iterable

import aiofiles
from fastapi import UploadFile

from open_pages.common import AppException, log
from open_pages.settings import SettingsDep


async def save_file(src: UploadFile, dst: Path, chunk_size: int) -> None:
    await src.seek(0)
    async with aiofiles.open(dst, "wb") as buffer:
        while True:
            contents = await src.read(chunk_size)
            if not contents:
                log.debug("File saved")
                break
            log.debug(f"Read {src.filename}: {len(contents)} bytes")
            await buffer.write(contents)


def get_files(site_name: str, settings: SettingsDep) -> Iterable[Path]:
    site_folder = settings.data_dir / site_name

    if (
        not site_folder.exists()
        or not site_folder.is_dir()
        or not any(site_folder.iterdir())
    ):
        raise AppException("Site not found")

    for f in site_folder.iterdir():
        if f.is_file():
            yield f


def get_sites(settings: SettingsDep) -> Iterable[str]:
    for f in settings.data_dir.iterdir():
        if f.is_dir():
            yield f.name
