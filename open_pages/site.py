from datetime import datetime
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ByteSize, PositiveInt, StringConstraints

from open_pages.common import AppException
from open_pages.files import get_files
from open_pages.settings import SettingsDep
from open_pages.utils import prettydate

SiteName = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_\-]+$")]


def get_existing_site(site_name: SiteName, settings: SettingsDep) -> Path:
    site_folder = settings.data_dir / site_name

    if (
        not site_folder.exists()
        or not site_folder.is_dir()
        or not any(site_folder.iterdir())
    ):
        raise AppException("Site not found")

    return site_folder


class SiteInfo(BaseModel):
    name: SiteName
    size: Annotated[int, ByteSize]
    number_of_files: PositiveInt
    last_modified: datetime
    last_modified_pretty: str


def get_site_info(site_folder: Path) -> SiteInfo:
    size = 0
    number_of_files = 0
    for f in get_files(site_folder):
        number_of_files += 1
        size += f.stat().st_size
    last_modified = datetime.fromtimestamp(site_folder.stat().st_mtime)
    return SiteInfo(
        name=site_folder.name,
        size=size,
        number_of_files=number_of_files,
        last_modified=last_modified,
        last_modified_pretty=prettydate(last_modified),
    )
