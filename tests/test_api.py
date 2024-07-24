def test_no_files(client) -> None:
    resp = client.post("/api/sites/simple_site")
    assert resp.status_code == 422


def test_invalid_filename(client) -> None:
    resp = client.post("/api/sites/&asd")
    assert resp.status_code == 422


def test_list_files(client, test_site, file_names) -> None:
    resp = client.get(f"/api/sites/{test_site}")
    assert resp.status_code == 200
    assert resp.json() == file_names
