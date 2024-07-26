from pathlib import Path
from typing import Annotated

from pydantic import StringConstraints

from open_pages.common import AppException
from open_pages.settings import SettingsDep

SiteName = Annotated[str, StringConstraints(pattern=r"^[a-zA-Z0-9_\-]+$")]


def existing_site(site_name: SiteName, settings: SettingsDep) -> Path:
    site_folder = settings.data_dir / site_name

    if (
        not site_folder.exists()
        or not site_folder.is_dir()
        or not any(site_folder.iterdir())
    ):
        raise AppException("Site not found")

    return site_folder
