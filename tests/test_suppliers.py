import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "v2", "api"))

from models.suppliers import Suppliers  # pylint: disable=wrong-import-position

# Kleine, vaste testdata: 3 suppliers.
TEST_SUPPLIERS = [
    {"id": 1, "code": "SUP-0001", "name": "FrieslandCampina", "city": "Amersfoort"},
    {"id": 2, "code": "SUP-0002", "name": "Unilever", "city": "Rotterdam"},
    {"id": 3, "code": "SUP-0003", "name": "Heineken", "city": "Amsterdam"},
]


@pytest.fixture
def suppliers(tmp_path):
    """Maak een Suppliers-model met de 3 test-suppliers in een tijdelijke map."""
    (tmp_path / "supplier.json").write_text(json.dumps(TEST_SUPPLIERS), encoding="utf-8")
    return Suppliers(str(tmp_path) + os.sep)


# get_suppliers

def test_get_suppliers_good(suppliers):
    """Goed: alle suppliers komen terug."""
    assert suppliers.get_suppliers() == TEST_SUPPLIERS


def test_get_suppliers_bad_empty_file(tmp_path):
    """Slecht: een leeg bestand geeft een lege lijst (geen fout)."""
    (tmp_path / "supplier.json").write_text("[]", encoding="utf-8")
    assert Suppliers(str(tmp_path) + os.sep).get_suppliers() == []
