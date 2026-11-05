import json

from models.base import Base

ITEM_LINES = []

class ItemLines(Base):
    def __init__(self, root_path, is_debug=False):
        self.data_path = root_path + "item_line.json"
        self.load(is_debug)

    def get_item_lines(self):
        """Geef de lijst met alle item lines."""
        return self.data

    def get_item_line(self, item_line_id):
        """Geef de item line met dit id, of None als die niet bestaat."""
        for item_line in self.data:
            if item_line["id"] == item_line_id:
                return item_line
        return None

    def add_item_line(self, item_line):
        item_line["created_at"] = self.get_timestamp()
        item_line["updated_at"] = self.get_timestamp()
        self.data.append(item_line)

    def update_item_line(self, item_line_id, item_line):
        item_line["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == item_line_id:
                self.data[i] = item_line
                break

    def remove_item_line(self, item_line_id):
        for x in self.data:
            if x["id"] == item_line_id:
                self.data.remove(x)

    def load(self, is_debug):
        if is_debug:
            self.data = ITEM_LINES
        else:
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f)