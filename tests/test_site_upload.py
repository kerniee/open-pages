def test_site(client, index_html, index_css, index_js) -> None:
    # Upload files
    files = [
        ("index.html", index_html),
        ("index.css", index_css),
        ("index.js", index_js),
        ("index.js", index_js),  # Test duplicate file
    ]
    resp = client.post("/api/sites/simple_site", files=[("files", f) for f in files])
    assert resp.status_code == 200

    # List files
    resp = client.get("/api/sites/simple_site")
    assert resp.status_code == 200
    assert resp.json() == ["index.html", "index.css", "index.js"]

    # Visit site
    resp = client.get("/sites/simple_site")
    assert resp.status_code == 200
    assert resp.text == index_html


def test_no_files(client) -> None:
    resp = client.post("/api/sites/simple_site")
    assert resp.status_code == 422


def test_invalid_filename(client) -> None:
    resp = client.post("/api/sites/&asd")
    assert resp.status_code == 422
