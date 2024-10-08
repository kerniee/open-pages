from collections import namedtuple
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator, TypeVar

from fastapi.testclient import TestClient
from pytest import fixture

from open_pages.main import app
from open_pages.settings import Settings, get_settings
from tests.api import upload_site

T = TypeVar("T")
YieldFixture = Generator[T, None, None]
SiteFiles = namedtuple("SiteFiles", ["filename", "file_contents"])


@fixture
def data_folder() -> YieldFixture[Path]:
    with TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@fixture
def client(data_folder: Path) -> TestClient:
    app.dependency_overrides[get_settings] = lambda: Settings(data_dir=data_folder)
    app.data_folder = data_folder  # type: ignore # Just for debugging
    return TestClient(app)


@fixture(scope="session")
def files_folder() -> Path:
    return Path(__file__).parent / "files"


@fixture(scope="session")
def file_names() -> list[str]:
    return ["index.css", "index.html", "index.js"]


@fixture(scope="session")
def site_files(files_folder, file_names) -> list[SiteFiles]:
    result = []
    for file_name in file_names:
        with open(files_folder / file_name) as f:
            result.append(SiteFiles(file_name, f.read()))
    return result


@fixture
def test_site(client, site_files) -> str:
    site_name = "simple_site"
    resp = upload_site(client, site_name, site_files)
    assert resp.status_code == 200

    return site_name
