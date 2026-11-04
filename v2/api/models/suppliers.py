import json

from models.base import Base

SUPPLIERS = []

class Suppliers(Base):
    def __init__(self, root_path, is_debug=False):
        self.data_path = root_path + "supplier.json"
        self.load(is_debug)

    def get_suppliers(self):
        """Geef de lijst met alle suppliers."""
        return self.data

    def get_supplier(self, supplier_id):
        """Geef de supplier met dit id, of None als die niet bestaat."""
        for supplier in self.data:
            if supplier["id"] == supplier_id:
                return supplier
        return None

    def add_supplier(self, supplier):
        supplier["created_at"] = self.get_timestamp()
        supplier["updated_at"] = self.get_timestamp()
        self.data.append(supplier)

    def update_supplier(self, supplier_id, supplier):
        supplier["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == supplier_id:
                self.data[i] = supplier
                break

    def remove_supplier(self, supplier_id):
        for x in self.data:
            if x["id"] == supplier_id:
                self.data.remove(x)

    def load(self, is_debug):
        if is_debug:
            self.data = SUPPLIERS
        else:
            with open(self.data_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f)