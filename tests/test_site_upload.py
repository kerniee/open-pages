def test_site(client, index_html, index_css, index_js):
    files = [index_html, index_css, index_js]
    resp = client.post("/sites/simple_site", files=[("files", f) for f in files])
    assert resp.status_code == 200


def test_no_files(client):
    resp = client.post("/sites/simple_site")
    assert resp.status_code == 422


def test_invalid_filename(client):
    resp = client.post("/sites/&asd")
    assert resp.status_code == 422
