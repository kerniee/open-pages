def test_visit_site(client, test_site, site_files) -> None:
    resp = client.get("/sites/simple_site")
    assert resp.status_code == 200
    index_html = next(f.file_contents for f in site_files if f.filename == "index.html")
    assert resp.text == index_html


def test_visit_site_with_referrer(client, test_site, site_files) -> None:
    resp = client.get(
        "/index.css", headers={"referer": "http://testserver/sites/simple_site"}
    )
    assert resp.status_code == 200
    index_css = next(f.file_contents for f in site_files if f.filename == "index.css")
    assert resp.text == index_css


def test_visit_site_with_invalid_referrer(client, test_site) -> None:
    resp = client.get("/index.css", headers={"referer": "."})
    assert resp.status_code == 422
    resp = client.get("/index.css", headers={"referer": "http://testserver"})
    assert resp.status_code == 400
    resp = client.get("/index.css", headers={"referer": "http://testserver/sites"})
    assert resp.status_code == 400
    resp = client.get(
        "/index.css", headers={"referer": "http://testserver/sites/non_existent_site"}
    )
    assert resp.status_code == 400
    resp = client.get(
        "/index.css", headers={"referer": "http://wrong_baseurl/sites/simple_site"}
    )
    # This is a bug, should be 400.
    # Don't know how to fix properly without using BASE_URL env
    assert resp.status_code == 200


def test_non_existent_site(client) -> None:
    resp = client.get("/sites/non_existent_site")
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Site not found"}
