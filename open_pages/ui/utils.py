import re

from pydantic import HttpUrl

SITE_REGEX = re.compile(r"/sites/([^/\s]*).*")


def get_site_from_referer(referer: HttpUrl) -> str | None:
    path = referer.path
    if not path:
        return None

    match = SITE_REGEX.match(path)
    if not match:
        return None

    res = match.group(1)
    return res
