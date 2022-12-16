from attrs import define, frozen
from datetime import date


@frozen
class OrderLine:
    orderid: str
    sku: str
    qty: int


@define
class Batch:
    reference: str
    sku: str
    available_quantity: int
    eta: date | None

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.qty
