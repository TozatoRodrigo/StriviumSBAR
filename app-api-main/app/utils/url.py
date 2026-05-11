from urllib.parse import urlencode


def build_url(base_url: str, path: str, params: dict[str, str] | None = None) -> str:
    if params is None:
        params = {}

    query_string = urlencode(params)

    path_parts = [part for part in path.split("/") if part]
    clean_path = "/".join(path_parts)

    clean_base_url = base_url.rstrip("/")

    url = clean_base_url + "/" + clean_path
    if query_string:
        url += "?" + query_string

    return url
