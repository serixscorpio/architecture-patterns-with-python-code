from attrs import define, field, frozen
from datetime import date


@frozen
class OrderLine:
    orderid: str
    sku: str
    qty: int


@define(eq=False)
class Batch:
    reference: str
    sku: str
    _purchased_quantity: int
    eta: date | None
    _allocations: set[OrderLine] = field(init=False, factory=set)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self._purchased_quantity >= line.qty

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self):
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self):
        return self._purchased_quantity - self.allocated_quantity


def allocate(line: OrderLine, batches: list[Batch]):
    """Standalone allocate function."""
    batch = next(b for b in sorted(batches) if batch.can_allocate(line))
    batch.allocate(line)
    return batch.reference
