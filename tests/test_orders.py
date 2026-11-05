import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "v2", "api"))

from providers import data_provider
from models.orders import Orders


TEST_ORDERS = [
    {"id": 1, "client_id": 10, "ship_to_client_id": 20, "bill_to_client_id": 30},
    {"id": 2, "client_id": 20, "ship_to_client_id": 10, "bill_to_client_id": 30},
    {"id": 3, "client_id": 30, "ship_to_client_id": 30, "bill_to_client_id": 30},
]

TEST_ORDER_ITEMS = [
    {"id": 1, "order_id": 1, "item_id": 10, "amount": 5, "unit_price": 12},
    {"id": 2, "order_id": 1, "item_id": 11, "amount": 2},
    {"id": 3, "order_id": 2, "item_id": 12, "amount": 7},
]

EXPECTED_ORDERS = [
    {**TEST_ORDERS[0], "items": [{"item_id": 10, "amount": 5}, {"item_id": 11, "amount": 2}]},
    {**TEST_ORDERS[1], "items": [{"item_id": 12, "amount": 7}]},
    {**TEST_ORDERS[2], "items": []},
]


@pytest.fixture
def orders(tmp_path, monkeypatch):
    (tmp_path / "order.json").write_text(json.dumps(TEST_ORDERS), encoding="utf-8")
    (tmp_path / "order_item.json").write_text(json.dumps(TEST_ORDER_ITEMS), encoding="utf-8")
    monkeypatch.setattr(data_provider, "ROOT_PATH", str(tmp_path) + os.sep)
    return Orders(str(tmp_path) + os.sep)


@pytest.fixture
def empty_orders(orders, tmp_path):
    (tmp_path / "order.json").write_text("[]", encoding="utf-8")
    return Orders(str(tmp_path) + os.sep)


def test_get_orders_good(orders):
    assert orders.get_orders() == EXPECTED_ORDERS


def test_get_orders_empty(empty_orders):
    assert empty_orders.get_orders() == []


def test_get_order_good(orders):
    assert orders.get_order(2) == EXPECTED_ORDERS[1]


def test_get_order_bad_unknown_id(orders):
    assert orders.get_order(999) is None


def test_get_order_empty(empty_orders):
    assert empty_orders.get_order(1) is None


def test_get_order_without_items(orders):
    assert orders.get_order(3) == EXPECTED_ORDERS[2]

