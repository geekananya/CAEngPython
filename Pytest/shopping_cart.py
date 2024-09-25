class ShoppingCart:
    def __init__(self, max_size: int):
        self.items = []
        self.max_size = max_size

    def add(self, item: str):
        if self.size() == self.max_size:
            raise OverflowError("cannot add more items")
        self.items.append(item)

    def size(self):
        return len(self.items)

    def get_items(self):
        return self.items

    def get_available_size(self):
        return self.max_size - self.size()

    def get_total_price(self, price_map):           # price map is external data and should be validated
        total_price = 0
        for item in self.items:
            total_price += price_map.get(item)
        return total_price