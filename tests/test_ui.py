from bs4 import BeautifulSoup


def test_visit_main_page(client, test_site) -> None:
    resp = client.get("/")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.text, "html.parser")
    assert soup.title and soup.title.string == "Open Pages"
