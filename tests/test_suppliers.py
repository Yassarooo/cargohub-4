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


# get_supplier

def test_get_supplier_good(suppliers):
    """Goed: supplier 2 bestaat en komt terug."""
    assert suppliers.get_supplier(2) == TEST_SUPPLIERS[1]


def test_get_supplier_bad_unknown_id(suppliers):
    """Slecht: supplier 99 bestaat niet, dus None."""
    assert suppliers.get_supplier(99) is None


# add_supplier (POST)

def test_add_supplier_good(suppliers):
    """Goed: na toevoegen kan je supplier 4 opvragen."""
    suppliers.add_supplier({"id": 4, "code": "SUP-0004", "name": "Philips", "city": "Eindhoven"})

    result = suppliers.get_supplier(4)
    assert result["name"] == "Philips"
    assert result["created_at"] != ""
    assert len(suppliers.get_suppliers()) == 4


def test_add_supplier_saved(suppliers, tmp_path):
    """Goed: na save staat de nieuwe supplier ook in het bestand."""
    suppliers.add_supplier({"id": 4, "code": "SUP-0004", "name": "Philips", "city": "Eindhoven"})
    suppliers.save()

    reloaded = Suppliers(str(tmp_path) + os.sep)
    assert reloaded.get_supplier(4)["name"] == "Philips"


def test_add_supplier_bad_not_saved_without_save(suppliers, tmp_path):
    """Slecht: zonder save komt de supplier niet in het bestand."""
    suppliers.add_supplier({"id": 4, "code": "SUP-0004", "name": "Philips", "city": "Eindhoven"})

    reloaded = Suppliers(str(tmp_path) + os.sep)
    assert reloaded.get_supplier(4) is None


# update_supplier (PUT)

def test_update_supplier_good(suppliers):
    """Goed: na wijzigen geeft get de nieuwe stad terug."""
    suppliers.update_supplier(2, {"id": 2, "code": "SUP-0002", "name": "Unilever", "city": "Utrecht"})

    result = suppliers.get_supplier(2)
    assert result["city"] == "Utrecht"
    assert result["updated_at"] != ""


def test_update_supplier_saved(suppliers, tmp_path):
    """Goed: na save staat de wijziging ook in het bestand."""
    suppliers.update_supplier(2, {"id": 2, "code": "SUP-0002", "name": "Unilever", "city": "Utrecht"})
    suppliers.save()

    reloaded = Suppliers(str(tmp_path) + os.sep)
    assert reloaded.get_supplier(2)["city"] == "Utrecht"


def test_update_supplier_bad_unknown_id(suppliers):
    """Slecht: supplier 99 bestaat niet, er verandert niks."""
    suppliers.update_supplier(99, {"id": 99, "code": "SUP-0099", "name": "Onbekend"})

    assert suppliers.get_supplier(99) is None
    assert len(suppliers.get_suppliers()) == 3
