from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship




DATABASE_URL = "postgresql+psycopg://admin:admin@localhost:5433/cargohub"

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    """Base class used to collect the database tables."""




class TimestampMixin:
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Warehouse(TimestampMixin, Base):
    __tablename__ = "warehouse"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str | None] = mapped_column(String)
    name: Mapped[str | None] = mapped_column(String)
    address: Mapped[str | None] = mapped_column(String)
    city: Mapped[str | None] = mapped_column(String)
    zip_code: Mapped[str | None] = mapped_column(String)
    province: Mapped[str | None] = mapped_column(String)
    country: Mapped[str | None] = mapped_column(String)
    contact_name: Mapped[str | None] = mapped_column(String)
    contact_phone: Mapped[str | None] = mapped_column(String)
    contact_email: Mapped[str | None] = mapped_column(String)
    locations: Mapped[list[Location]] = relationship(back_populates="warehouse")
    orders: Mapped[list[Order]] = relationship(back_populates="warehouse")


class Location(TimestampMixin, Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouse.id"))
    code: Mapped[str | None] = mapped_column(String)
    name: Mapped[str | None] = mapped_column(String)
    warehouse: Mapped[Warehouse | None] = relationship(back_populates="locations")
    inventories: Mapped[list[Inventory]] = relationship(back_populates="location")
    transfers_from: Mapped[list[Transfer]] = relationship(
        back_populates="from_location", foreign_keys="Transfer.from_location_id"
    )
    transfers_to: Mapped[list[Transfer]] = relationship(
        back_populates="to_location", foreign_keys="Transfer.to_location_id"
    )


class ItemLine(TimestampMixin, Base):
    __tablename__ = "item_line"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    items: Mapped[list[Item]] = relationship(back_populates="item_line")


class ItemGroup(TimestampMixin, Base):
    __tablename__ = "item_group"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    items: Mapped[list[Item]] = relationship(back_populates="item_group")


class ItemType(TimestampMixin, Base):
    __tablename__ = "item_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    items: Mapped[list[Item]] = relationship(back_populates="item_type")


class Supplier(TimestampMixin, Base):
    __tablename__ = "supplier"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str | None] = mapped_column(String)
    name: Mapped[str | None] = mapped_column(String)
    address: Mapped[str | None] = mapped_column(String)
    city: Mapped[str | None] = mapped_column(String)
    zip_code: Mapped[str | None] = mapped_column(String)
    province: Mapped[str | None] = mapped_column(String)
    country: Mapped[str | None] = mapped_column(String)
    contact_name: Mapped[str | None] = mapped_column(String)
    phone_number: Mapped[str | None] = mapped_column(String)
    reference: Mapped[str | None] = mapped_column(String)
    items: Mapped[list[Item]] = relationship(back_populates="supplier")


class Item(TimestampMixin, Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str | None] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(String)
    barcode: Mapped[str | None] = mapped_column(String)
    model_number: Mapped[str | None] = mapped_column(String)
    commodity_code: Mapped[int | None] = mapped_column(Integer)
    unit_weight: Mapped[float | None] = mapped_column(Numeric(12, 3))
    item_line_id: Mapped[int | None] = mapped_column(ForeignKey("item_line.id"))
    item_group_id: Mapped[int | None] = mapped_column(ForeignKey("item_group.id"))
    item_type_id: Mapped[int | None] = mapped_column(ForeignKey("item_type.id"))
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("supplier.id"))
    supplier_sku: Mapped[str | None] = mapped_column(String)
    min_purchase_qty: Mapped[int | None] = mapped_column(Integer)
    case_size: Mapped[int | None] = mapped_column(Integer)
    packaging_type: Mapped[str | None] = mapped_column(String)
    order_multiple: Mapped[int | None] = mapped_column(Integer)
    item_line: Mapped[ItemLine | None] = relationship(back_populates="items")
    item_group: Mapped[ItemGroup | None] = relationship(back_populates="items")
    item_type: Mapped[ItemType | None] = relationship(back_populates="items")
    supplier: Mapped[Supplier | None] = relationship(back_populates="items")
    inventories: Mapped[list[Inventory]] = relationship(back_populates="item")
    order_items: Mapped[list[OrderItem]] = relationship(back_populates="item")
    shipment_items: Mapped[list[ShipmentItem]] = relationship(back_populates="item")
    transfer_items: Mapped[list[TransferItem]] = relationship(back_populates="item")


class Inventory(TimestampMixin, Base):
    __tablename__ = "inventory"
    __table_args__ = (UniqueConstraint("item_id", "location_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    quantity_on_hand: Mapped[int | None] = mapped_column(Integer)
    quantity_expected: Mapped[int | None] = mapped_column(Integer)
    quantity_ordered: Mapped[int | None] = mapped_column(Integer)
    quantity_allocated: Mapped[int | None] = mapped_column(Integer)
    item: Mapped[Item] = relationship(back_populates="inventories")
    location: Mapped[Location] = relationship(back_populates="inventories")


class Client(TimestampMixin, Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str | None] = mapped_column(String)
    address: Mapped[str | None] = mapped_column(String)
    city: Mapped[str | None] = mapped_column(String)
    zip_code: Mapped[str | None] = mapped_column(String)
    province: Mapped[str | None] = mapped_column(String)
    country: Mapped[str | None] = mapped_column(String)
    contact_name: Mapped[str | None] = mapped_column(String)
    contact_phone: Mapped[str | None] = mapped_column(String)
    contact_email: Mapped[str | None] = mapped_column(String)
    orders: Mapped[list[Order]] = relationship(
        back_populates="client", foreign_keys="Order.client_id"
    )
    ship_to_orders: Mapped[list[Order]] = relationship(
        back_populates="ship_to_client", foreign_keys="Order.ship_to_client_id"
    )
    bill_to_orders: Mapped[list[Order]] = relationship(
        back_populates="bill_to_client", foreign_keys="Order.bill_to_client_id"
    )


class Order(TimestampMixin, Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int | None] = mapped_column(ForeignKey("client.id"))
    ship_to_client_id: Mapped[int | None] = mapped_column(ForeignKey("client.id"))
    bill_to_client_id: Mapped[int | None] = mapped_column(ForeignKey("client.id"))
    warehouse_id: Mapped[int | None] = mapped_column(ForeignKey("warehouse.id"))
    reference: Mapped[str | None] = mapped_column(String)
    customer_po_number: Mapped[str | None] = mapped_column(String)
    order_status: Mapped[str | None] = mapped_column(String)
    shipping_notes: Mapped[str | None] = mapped_column(String)
    order_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    request_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    client: Mapped[Client | None] = relationship(
        back_populates="orders", foreign_keys=[client_id]
    )
    ship_to_client: Mapped[Client | None] = relationship(
        back_populates="ship_to_orders", foreign_keys=[ship_to_client_id]
    )
    bill_to_client: Mapped[Client | None] = relationship(
        back_populates="bill_to_orders", foreign_keys=[bill_to_client_id]
    )
    warehouse: Mapped[Warehouse | None] = relationship(back_populates="orders")
    items: Mapped[list[OrderItem]] = relationship(back_populates="order")
    shipments: Mapped[list[Shipment]] = relationship(back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    amount: Mapped[int | None] = mapped_column(Integer)
    unit_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    order: Mapped[Order] = relationship(back_populates="items")
    item: Mapped[Item] = relationship(back_populates="order_items")


class Shipment(TimestampMixin, Base):
    __tablename__ = "shipment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int | None] = mapped_column(ForeignKey("order.id"))
    reference: Mapped[str | None] = mapped_column(String)
    shipment_type: Mapped[str | None] = mapped_column(String)
    shipment_status: Mapped[str | None] = mapped_column(String)
    carrier_name: Mapped[str | None] = mapped_column(String)
    shipping_method: Mapped[str | None] = mapped_column(String)
    payment_type: Mapped[str | None] = mapped_column(String)
    shipment_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    order: Mapped[Order | None] = relationship(back_populates="shipments")
    items: Mapped[list[ShipmentItem]] = relationship(back_populates="shipment")


class ShipmentItem(Base):
    __tablename__ = "shipment_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    shipment_id: Mapped[int] = mapped_column(ForeignKey("shipment.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    amount: Mapped[int | None] = mapped_column(Integer)
    shipment: Mapped[Shipment] = relationship(back_populates="items")
    item: Mapped[Item] = relationship(back_populates="shipment_items")


class Transfer(TimestampMixin, Base):
    __tablename__ = "transfer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_location_id: Mapped[int | None] = mapped_column(ForeignKey("location.id"))
    to_location_id: Mapped[int | None] = mapped_column(ForeignKey("location.id"))
    reference: Mapped[str | None] = mapped_column(String)
    transfer_status: Mapped[str | None] = mapped_column(String)
    from_location: Mapped[Location | None] = relationship(
        back_populates="transfers_from", foreign_keys=[from_location_id]
    )
    to_location: Mapped[Location | None] = relationship(
        back_populates="transfers_to", foreign_keys=[to_location_id]
    )
    items: Mapped[list[TransferItem]] = relationship(back_populates="transfer")


class TransferItem(Base):
    __tablename__ = "transfer_item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    transfer_id: Mapped[int] = mapped_column(ForeignKey("transfer.id"))
    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    amount: Mapped[int | None] = mapped_column(Integer)
    transfer: Mapped[Transfer] = relationship(back_populates="items")
    item: Mapped[Item] = relationship(back_populates="transfer_items")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    api_key: Mapped[str] = mapped_column(String, unique=True)
    app: Mapped[str | None] = mapped_column(String)
    endpoint_access: Mapped[list[EndpointAccess]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class EndpointAccess(Base):
    __tablename__ = "endpoint_access"
    __table_args__ = (UniqueConstraint("user_id", "resource"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    resource: Mapped[str] = mapped_column(String)
    can_get: Mapped[bool] = mapped_column(Boolean, default=False)
    can_post: Mapped[bool] = mapped_column(Boolean, default=False)
    can_put: Mapped[bool] = mapped_column(Boolean, default=False)
    can_delete: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped[User] = relationship(back_populates="endpoint_access")


def create_database():
    Base.metadata.create_all(engine)

create_database()

