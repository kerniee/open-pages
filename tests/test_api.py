from tests.api import upload_site
from tests.conftest import SiteFiles


def test_upload_one_file(client, test_site, site_files) -> None:
    resp = upload_site(client, "simple_site", [site_files[0]])
    assert resp.status_code == 200


def test_no_files(client) -> None:
    resp = upload_site(client, "simple_site", [])
    assert resp.status_code == 422


def test_invalid_filename(client, site_files) -> None:
    resp = upload_site(client, "simple_site", [site_files[0]._replace(filename=".")])
    assert resp.status_code == 400


def test_list_files(client, test_site, file_names) -> None:
    resp = client.get(f"/api/sites/{test_site}/files")
    assert resp.status_code == 200
    assert resp.json() == file_names


def test_list_non_existent_site(client, test_site, file_names) -> None:
    resp = client.get("/api/sites/non_existent_site")
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Site not found"}


def test_with_subpath(client, site_files) -> None:
    subpath_file_paths = [
        SiteFiles("subpath/" + f.filename, f.file_contents) for f in site_files
    ]

    resp = upload_site(client, "subpath_site", subpath_file_paths)
    assert resp.status_code == 200


def test_delete(client, test_site) -> None:
    resp = client.delete(f"/api/sites/{test_site}")
    assert resp.status_code == 200

    resp = client.get(f"/api/sites/{test_site}")
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Site not found"}

    resp = client.delete(f"/api/sites/{test_site}")
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Site not found"}
