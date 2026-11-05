import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "v2", "api"))

from models.item_lines import ItemLines  

# Kleine, vaste testdata: 3 item lines.
TEST_ITEM_LINES = [
    {"id": 1, "name": "Zuivel", "description": "Melk, kaas en yoghurt"},
    {"id": 2, "name": "Diepvries", "description": "Diepvriesproducten"},
    {"id": 3, "name": "Brood", "description": "Brood en banket"},
]

@pytest.fixture
def item_lines(tmp_path):
    """Maak een ItemLines-model met de 3 test-item-lines in een tijdelijke map."""
    (tmp_path / "item_line.json").write_text(json.dumps(TEST_ITEM_LINES), encoding="utf-8")
    return ItemLines(str(tmp_path) + os.sep)

# get_item_lines

def test_get_item_lines_good(item_lines):
    """Goed: alle item lines komen terug."""
    assert item_lines.get_item_lines() == TEST_ITEM_LINES


def test_get_item_lines_bad_empty_file(tmp_path):
    """Slecht: een leeg bestand geeft een lege lijst (geen fout)."""
    (tmp_path / "item_line.json").write_text("[]", encoding="utf-8")
    assert ItemLines(str(tmp_path) + os.sep).get_item_lines() == []

# get_item_line

def test_get_item_line_good(item_lines):
    """Goed: item line 2 bestaat en komt terug."""
    assert item_lines.get_item_line(2) == TEST_ITEM_LINES[1]


def test_get_item_line_bad_unknown_id(item_lines):
    """Slecht: item line 99 bestaat niet, dus None."""
    assert item_lines.get_item_line(99) is None
