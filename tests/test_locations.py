import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "v2", "api"),
)
from models.locations import Locations

TEST_LOCATIONS = [
    {"id": 1, "warehouse_id": 10, "code": "A-01"},
    {"id": 2, "warehouse_id": 20, "code": "B-01"},
    {"id": 3, "warehouse_id": 10, "code": "A-02"},
]


@pytest.fixture
def locations(tmp_path):
    data_file = tmp_path / "location.json"
    data_file.write_text(
        json.dumps(TEST_LOCATIONS),
        encoding="utf-8",
    )

    return Locations(str(tmp_path) + os.sep)

def test_get_location_good(locations):
    result = locations.get_location(2)

    assert result == TEST_LOCATIONS[1]

def test_get_location_bad_unknown_id(locations):
    result = locations.get_location(999)

    assert result is None