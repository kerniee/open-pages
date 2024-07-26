import functools
from typing import Annotated

from fastapi import Depends
from pydantic import DirectoryPath
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    data_dir: DirectoryPath = DirectoryPath("data")

    chunk_size: int = 2**20  # 1 MB
    catch_exceptions: bool = True


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
