
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

STRIP_PARAMS = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content","gclid","fbclid","cmpid","irgwc"}

def normalize(url: str, force_locale: str | None = None) -> str:
    u = urlparse(url)
    # drop tracking params
    q = [(k,v) for k,v in parse_qsl(u.query, keep_blank_values=True) if k not in STRIP_PARAMS]
    path = u.path
    if force_locale and not path.startswith(f"/{force_locale}/"):
        path = f"/{force_locale.rstrip('/')}{path}"
    return urlunparse((u.scheme, u.netloc, path, "", urlencode(q), ""))
