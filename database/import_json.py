"""Import the v1 JSON data into the SQLAlchemy PostgreSQL schema."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import Session

from models import (
    Base,
    Client,
    EndpointAccess,
    Inventory,
    Item,
    ItemGroup,
    ItemLine,
    ItemType,
    Location,
    Order,
    OrderItem,
    Shipment,
    ShipmentItem,
    Supplier,
    Transfer,
    TransferItem,
    User,
    Warehouse,
)

DATABASE_URL = "postgresql+psycopg://admin:admin@localhost:5433/cargohub"
engine = create_engine(DATABASE_URL)


TABLES = (
    Warehouse,
    Location,
    ItemLine,
    ItemGroup,
    ItemType,
    Supplier,
    Item,
    Inventory,
    Client,
    Order,
    OrderItem,
    Shipment,
    ShipmentItem,
    Transfer,
    TransferItem,
    User,
    EndpointAccess,
)


def read_rows(data_dir: Path, filename: str) -> list[dict[str, Any]]:
    with (data_dir / filename).open(encoding="utf-8") as data_file:
        rows = json.load(data_file)
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{filename} must contain a JSON array of objects")
    return rows


def parse_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def rows_for_model(data_dir: Path, filename: str, model: type[Any]) -> list[Any]:
    result = []
    for row in read_rows(data_dir, filename):
        values = dict(row)
        for field in ("created_at", "updated_at", "order_date", "request_date", "shipment_date"):
            if field in values:
                values[field] = parse_datetime(values[field])
        result.append(model(**values))
    return result


def import_json_data(data_dir: Path, replace: bool = False) -> None:
    """Import every v1 JSON file in one transaction."""
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        if replace:
            for model in reversed(TABLES):
                session.execute(delete(model))

        files_and_models = (
            ("warehouse.json", Warehouse),
            ("location.json", Location),
            ("item_line.json", ItemLine),
            ("item_group.json", ItemGroup),
            ("item_type.json", ItemType),
            ("supplier.json", Supplier),
            ("item.json", Item),
            ("inventory.json", Inventory),
            ("client.json", Client),
            ("order.json", Order),
            ("order_item.json", OrderItem),
            ("shipment.json", Shipment),
            ("shipment_item.json", ShipmentItem),
            ("transfer.json", Transfer),
            ("transfer_item.json", TransferItem),
        )
        for filename, model in files_and_models:
            session.add_all(rows_for_model(data_dir, filename, model))

        for user_id, row in enumerate(read_rows(data_dir, "user.json"), start=1):
            permissions = row.get("endpoint_access", {})
            user = User(id=user_id, api_key=row["api_key"], app=row.get("app"))
            user.endpoint_access = [
                EndpointAccess(
                    resource=resource,
                    can_get=bool(values.get("get", False)),
                    can_post=bool(values.get("post", False)),
                    can_put=bool(values.get("put", False)),
                    can_delete=bool(values.get("delete", False)),
                )
                for resource, values in permissions.items()
            ]
            session.add(user)

        session.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "v1" / "data",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete existing rows before importing the JSON data.",
    )
    args = parser.parse_args()
    import_json_data(args.data_dir, replace=args.replace)
    print("JSON import completed.")


if __name__ == "__main__":
    main()
