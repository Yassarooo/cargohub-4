import json
import os
import sys

import pytest

# Zodat "from models.items import Items" werkt, net als in v2/api/main.py.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "v2", "api"))

from models.items import Items  # pylint: disable=wrong-import-position

# Kleine, vaste testdata: 3 items.
TEST_ITEMS = [
    {"id": 1, "item_line_id": 1, "item_group_id": 1, "item_type_id": 1, "supplier_id": 10},
    {"id": 2, "item_line_id": 2, "item_group_id": 1, "item_type_id": 2, "supplier_id": 10},
    {"id": 3, "item_line_id": 1, "item_group_id": 2, "item_type_id": 1, "supplier_id": 11},
]


@pytest.fixture
def items(tmp_path):
    """Maak een Items-model met de 3 test-items in een tijdelijke map."""
    (tmp_path / "item.json").write_text(json.dumps(TEST_ITEMS), encoding="utf-8")
    return Items(str(tmp_path) + os.sep)


# get_items

def test_get_items_good(items):
    """Goed: alle items komen terug."""
    assert items.get_items() == TEST_ITEMS


def test_get_items_bad_empty_file(tmp_path):
    """Slecht: een leeg bestand geeft een lege lijst (geen fout)."""
    (tmp_path / "item.json").write_text("[]", encoding="utf-8")
    assert Items(str(tmp_path) + os.sep).get_items() == []


# get_item

def test_get_item_good(items):
    """Goed: item 2 bestaat en komt terug."""
    assert items.get_item(2) == TEST_ITEMS[1]


def test_get_item_bad_unknown_id(items):
    """Slecht: item 99 bestaat niet, dus None."""
    assert items.get_item(99) is None


# get_items_for_item_line

def test_get_items_for_item_line_good(items):
    """Goed: item line 1 bevat de items 1 en 3 (alleen de id's)."""
    assert items.get_items_for_item_line(1) == [1, 3]


def test_get_items_for_item_line_bad_unknown_id(items):
    """Slecht: item line 99 bestaat niet, dus een lege lijst."""
    assert items.get_items_for_item_line(99) == []


# get_items_for_item_group

def test_get_items_for_item_group_good(items):
    """Goed: item group 1 bevat de items 1 en 2 (alleen de id's)."""
    assert items.get_items_for_item_group(1) == [1, 2]


def test_get_items_for_item_group_bad_unknown_id(items):
    """Slecht: item group 99 bestaat niet, dus een lege lijst."""
    assert items.get_items_for_item_group(99) == []


# get_items_for_item_type

def test_get_items_for_item_type_good(items):
    """Goed: item type 2 bevat alleen item 2 (alleen het id)."""
    assert items.get_items_for_item_type(2) == [2]


def test_get_items_for_item_type_bad_unknown_id(items):
    """Slecht: item type 99 bestaat niet, dus een lege lijst."""
    assert items.get_items_for_item_type(99) == []


# get_items_for_supplier

def test_get_items_for_supplier_good(items):
    """Goed: leverancier 11 heeft item 3 (het hele item, niet alleen het id)."""
    assert items.get_items_for_supplier(11) == [TEST_ITEMS[2]]


def test_get_items_for_supplier_bad_unknown_id(items):
    """Slecht: leverancier 99 bestaat niet, dus een lege lijst."""
    assert items.get_items_for_supplier(99) == []
