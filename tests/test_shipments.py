import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "v2", "api"))

# data_provider eerst importeren, anders krijg je een circular import (zoals in main.py)
from providers import data_provider  # pylint: disable=wrong-import-position
from models.shipments import Shipments  # pylint: disable=wrong-import-position

# Kleine, vaste testdata: 3 shipments en hun items.
TEST_SHIPMENTS = [
    {"id": 1, "reference": "SHP-000001", "order_id": 1, "shipment_status": "Pending"},
    {"id": 2, "reference": "SHP-000002", "order_id": 2, "shipment_status": "Transit"},
    {"id": 3, "reference": "SHP-000003", "order_id": None, "shipment_status": "Delivered"},
]

TEST_SHIPMENT_ITEMS = [
    {"id": 1, "shipment_id": 1, "item_id": 10, "amount": 5},
    {"id": 2, "shipment_id": 1, "item_id": 11, "amount": 2},
    {"id": 3, "shipment_id": 2, "item_id": 10, "amount": 7},
]


@pytest.fixture
def shipments(tmp_path, monkeypatch):
    """Maak een Shipments-model met de testdata in een tijdelijke map."""
    (tmp_path / "shipment.json").write_text(json.dumps(TEST_SHIPMENTS), encoding="utf-8")
    (tmp_path / "shipment_item.json").write_text(
        json.dumps(TEST_SHIPMENT_ITEMS), encoding="utf-8"
    )
    # de items van een shipment komen via data_provider, die moet ook de tijdelijke map gebruiken
    monkeypatch.setattr(data_provider, "ROOT_PATH", str(tmp_path) + os.sep)
    return Shipments(str(tmp_path) + os.sep)


# get_shipments

def test_get_shipments_good(shipments):
    """Goed: alle 3 shipments komen terug, met hun items erbij."""
    result = shipments.get_shipments()

    assert len(result) == 3
    assert result[0]["reference"] == "SHP-000001"
    assert result[0]["items"] == [{"item_id": 10, "amount": 5}, {"item_id": 11, "amount": 2}]
    assert result[1]["items"] == [{"item_id": 10, "amount": 7}]


def test_get_shipments_no_items(shipments):
    """Shipment 3 heeft geen items, dus een lege lijst."""
    result = shipments.get_shipments()

    assert result[2]["items"] == []


# get_shipment

def test_get_shipment_good(shipments):
    """Goed: shipment 2 bestaat en komt terug met zijn items."""
    result = shipments.get_shipment(2)

    assert result["reference"] == "SHP-000002"
    assert result["items"] == [{"item_id": 10, "amount": 7}]


def test_get_shipment_bad_unknown_id(shipments):
    """Slecht: shipment 99 bestaat niet, dus None."""
    assert shipments.get_shipment(99) is None


# get_items_in_shipment

def test_get_items_in_shipment_good(shipments):
    """Goed: shipment 1 heeft 2 items."""
    result = shipments.get_items_in_shipment(1)

    assert result == [{"item_id": 10, "amount": 5}, {"item_id": 11, "amount": 2}]


def test_get_items_in_shipment_bad_unknown_id(shipments):
    """Slecht: shipment 99 bestaat niet, dus een lege lijst."""
    assert shipments.get_items_in_shipment(99) == []


# get_order_ids_in_shipment

def test_get_order_ids_in_shipment_good(shipments):
    """Goed: shipment 2 hoort bij order 2."""
    assert shipments.get_order_ids_in_shipment(2) == [2]


def test_get_order_ids_in_shipment_no_order(shipments):
    """Shipment 3 heeft geen order, dus een lege lijst."""
    assert shipments.get_order_ids_in_shipment(3) == []


def test_get_order_ids_in_shipment_bad_unknown_id(shipments):
    """Slecht: shipment 99 bestaat niet, dus een lege lijst."""
    assert shipments.get_order_ids_in_shipment(99) == []


# add_shipment (POST)

def test_add_shipment_good(shipments):
    """Goed: na toevoegen kan je shipment 4 opvragen."""
    shipments.add_shipment({"id": 4, "reference": "SHP-000004", "order_id": 3})

    result = shipments.get_shipment(4)
    assert result["reference"] == "SHP-000004"
    assert result["created_at"] != ""
    assert len(shipments.get_shipments()) == 4


def test_add_shipment_saved(shipments, tmp_path):
    """Goed: na save staat de nieuwe shipment ook in het bestand."""
    shipments.add_shipment({"id": 4, "reference": "SHP-000004", "order_id": 3})
    shipments.save()

    reloaded = Shipments(str(tmp_path) + os.sep)
    assert reloaded.get_shipment(4)["reference"] == "SHP-000004"


def test_add_shipment_bad_not_saved_without_save(shipments, tmp_path):
    """Slecht: zonder save komt de shipment niet in het bestand."""
    shipments.add_shipment({"id": 4, "reference": "SHP-000004", "order_id": 3})

    reloaded = Shipments(str(tmp_path) + os.sep)
    assert reloaded.get_shipment(4) is None


# update_shipment (PUT)

def test_update_shipment_good(shipments):
    """Goed: na wijzigen geeft get de nieuwe status terug."""
    shipments.update_shipment(
        1, {"id": 1, "reference": "SHP-000001", "order_id": 1, "shipment_status": "Delivered"}
    )

    result = shipments.get_shipment(1)
    assert result["shipment_status"] == "Delivered"
    assert result["updated_at"] != ""


def test_update_shipment_saved(shipments, tmp_path):
    """Goed: na save staat de wijziging ook in het bestand."""
    shipments.update_shipment(
        2, {"id": 2, "reference": "SHP-000002", "order_id": 2, "shipment_status": "Delivered"}
    )
    shipments.save()

    reloaded = Shipments(str(tmp_path) + os.sep)
    assert reloaded.get_shipment(2)["shipment_status"] == "Delivered"


def test_update_shipment_bad_unknown_id(shipments):
    """Slecht: shipment 99 bestaat niet, er verandert niks."""
    shipments.update_shipment(99, {"id": 99, "reference": "SHP-000099"})

    assert shipments.get_shipment(99) is None
    assert len(shipments.get_shipments()) == 3


# update_orders_in_shipment (PUT /shipments/{id}/orders)

def test_update_orders_in_shipment_good(shipments):
    """Goed: shipment 3 krijgt order 5."""
    shipments.update_orders_in_shipment(3, [5])

    assert shipments.get_order_ids_in_shipment(3) == [5]


def test_update_orders_in_shipment_empty_list(shipments):
    """Een lege lijst haalt de order weg bij shipment 1."""
    shipments.update_orders_in_shipment(1, [])

    assert shipments.get_order_ids_in_shipment(1) == []


def test_update_orders_in_shipment_bad_unknown_id(shipments):
    """Slecht: shipment 99 bestaat niet, er verandert niks."""
    shipments.update_orders_in_shipment(99, [5])

    assert shipments.get_order_ids_in_shipment(99) == []
    assert shipments.get_order_ids_in_shipment(1) == [1]


# remove_shipment (DELETE)

def test_remove_shipment_good(shipments):
    """Goed: na verwijderen is shipment 2 weg."""
    shipments.remove_shipment(2)

    assert shipments.get_shipment(2) is None
    assert len(shipments.get_shipments()) == 2


def test_remove_shipment_saved(shipments, tmp_path):
    """Goed: na save is shipment 2 ook uit het bestand weg."""
    shipments.remove_shipment(2)
    shipments.save()

    reloaded = Shipments(str(tmp_path) + os.sep)
    assert reloaded.get_shipment(2) is None


def test_remove_shipment_bad_unknown_id(shipments):
    """Slecht: shipment 99 bestaat niet, de andere 3 blijven staan."""
    shipments.remove_shipment(99)

    assert len(shipments.get_shipments()) == 3
