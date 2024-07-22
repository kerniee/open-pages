import functools

from pydantic import DirectoryPath
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    data_dir: DirectoryPath = DirectoryPath("data")

    chunk_size: int = 2**20  # 1 MB


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
