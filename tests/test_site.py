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
