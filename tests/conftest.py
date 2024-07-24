from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator, TypeVar

from fastapi.testclient import TestClient
from pytest import fixture

from open_pages.main import app
from open_pages.settings import Settings, get_settings

T = TypeVar("T")
YieldFixture = Generator[T, None, None]


@fixture
def data_folder() -> YieldFixture[Path]:
    with TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@fixture
def client(data_folder: Path) -> TestClient:
    app.dependency_overrides[get_settings] = lambda: Settings(data_dir=data_folder)
    return TestClient(app)


@fixture(scope="session")
def files_folder() -> Path:
    return Path(__file__).parent / "files"


@fixture(scope="session")
def index_html(files_folder: Path) -> str:
    with open(files_folder / "index.html") as f:
        return f.read()


@fixture(scope="session")
def index_css(files_folder: Path) -> str:
    with open(files_folder / "index.css") as f:
        return f.read()


@fixture(scope="session")
def index_js(files_folder: Path) -> str:
    with open(files_folder / "index.js") as f:
        return f.read()
