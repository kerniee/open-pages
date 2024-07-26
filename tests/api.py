from typing import Iterable

from httpx import Client, Response
from httpx._types import FileTypes


def upload_site(client: Client, site_name: str, files: Iterable[FileTypes]) -> Response:
    _files = [("name", (None, site_name))] + [("files", f) for f in files]

    resp = client.post("/api/sites", files=_files)
    return resp
