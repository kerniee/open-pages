from pathlib import Path

import aiofiles
from fastapi import UploadFile

from open_pages.log import log


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
