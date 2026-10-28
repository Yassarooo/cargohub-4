import json

from models.base import Base

ITEMS = []

class Items(Base):
    def __init__(self, root_path, is_debug=False):
        self.data_path = root_path + "item.json"
        self.load(is_debug)

    def get_items(self):
        """Geef de lijst met alle items."""
        return self.data

    def get_item(self, item_id):
        """Geef het item met dit id, of None als het niet bestaat."""
        for item in self.data:
            if item["id"] == item_id:
                return item
        return None

    def get_items_for_item_line(self, item_line_id):
        """Geef de id's van alle items in deze item line."""
        return self.get_item_ids_where("item_line_id", item_line_id)

    def get_items_for_item_group(self, item_group_id):
        """Geef de id's van alle items in deze item group."""
        return self.get_item_ids_where("item_group_id", item_group_id)

    def get_items_for_item_type(self, item_type_id):
        """Geef de id's van alle items van dit item type."""
        return self.get_item_ids_where("item_type_id", item_type_id)

    def get_items_for_supplier(self, supplier_id):
        """Geef de volledige items (niet alleen id's) van deze leverancier."""
        return [item for item in self.data if item["supplier_id"] == supplier_id]

    def get_item_ids_where(self, field, value):
        """Geef de id's van alle items waarbij field gelijk is aan value."""
        return [item["id"] for item in self.data if item[field] == value]

    def add_item(self, item):
        item["created_at"] = self.get_timestamp()
        item["updated_at"] = self.get_timestamp()
        self.data.append(item)

    def update_item(self, item_id, item):
        item["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == item_id:
                self.data[i] = item
                break

    def remove_item(self, item_id):
        for x in self.data:
            if x["id"] == item_id:
                self.data.remove(x)

    def load(self, is_debug):
        if is_debug:
            self.data = ITEMS
        else:
            f = open(self.data_path, "r")
            self.data = json.load(f)
            f.close()

    def save(self):
        f = open(self.data_path, "w")
        json.dump(self.data, f)
        f.close()