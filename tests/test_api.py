def test_no_files(client) -> None:
    files = [("name", (None, "simple_site"))]
    resp = client.post("/api/sites", files=files)
    assert resp.status_code == 422


def test_invalid_filename(client, site_files) -> None:
    files = [("files", f) for f in site_files] + [("name", "&abs")]
    resp = client.post("/api/sites", files=files)
    assert resp.status_code == 422
    errors = resp.json()["detail"]
    assert len(errors) == 1 and errors[0]["msg"] == "Input should be a valid string"


def test_list_files(client, test_site, file_names) -> None:
    resp = client.get(f"/api/sites/{test_site}")
    assert resp.status_code == 200
    assert resp.json() == file_names
