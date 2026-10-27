# test of the get all endpoints 200 ok returnen met een niet lege json body
# de api is langzaam en raakt snel overbelast

# python -m pytest  ---> runned alle pytests (moet in de cargohub-4 dir zitten)
# duurt heel lang trouwens om te runnen

import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

API_BASE_URL = "http://145.24.237.163:8000/api/v1"
API_KEY = "r2e4c6e8i0v3i5n7g9s"

GET_ALL_ENDPOINTS = [
    "/warehouses",
    "/locations",
    "/transfers",
    "/items",
    "/item_lines",
    "/item_groups",
    "/item_types",
    "/inventories",
    "/suppliers",
    "/orders",
    "/clients",
    "/shipments",
]

@pytest.mark.parametrize("path", GET_ALL_ENDPOINTS)
def test_get_all_returns_ok_and_nonempty_json(path):
    request = Request(
        f"{API_BASE_URL.rstrip('/')}{path}",
        headers={"API_KEY": API_KEY},
        method="GET",
    )

    try:
        with urlopen(request, timeout=30) as response:
            status_code = response.status
            content_type = response.headers.get("Content-Type", "")
            body = response.read()
    except HTTPError as error:
        status_code = error.code
        content_type = error.headers.get("Content-Type", "")
        body = error.read()

    assert status_code == 200, f"GET {path} returned {status_code}: {body!r}"
    assert content_type.lower().startswith("application/json")

    payload = json.loads(body)
    assert payload, f"GET {path} returned an empty JSON body"