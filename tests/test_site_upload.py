def test_site(client, index_html, index_css, index_js):
    files = [index_html, index_css, index_js]
    resp = client.post("/api/sites/simple_site", files=[("files", f) for f in files])
    assert resp.status_code == 200

    resp = client.get("/api/sites/simple_site")
    assert resp.status_code == 200
    assert resp.json() == ["index.html", "index.css", "index.js"]


def test_no_files(client):
    resp = client.post("/api/sites/simple_site")
    assert resp.status_code == 422


def test_invalid_filename(client):
    resp = client.post("/api/sites/&asd")
    assert resp.status_code == 422
