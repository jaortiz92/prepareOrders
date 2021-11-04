from typing import List, Any, Callable, Dict


class Prices:
    id = 0

    def __init__(self, reference: str, size: str, collection: str, price: int, cost: int) -> None:
        self.reference: str = reference
        self.size: str = size
        self.collection: str = collection
        self.price: int = int(price)
        self.cost: int = int(cost)

    def row(self):
        row: Dict[str, Any] = {
            'id': self.id,
            'REFERENCIA': self.reference,
            'TALLAS': self.size,
            'PRECIO UND': self.price,
            'COLECCIÓN': self.collection,
            'COSTO': self.cost
        }
        return row
