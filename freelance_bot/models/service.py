class Service:
    def __init__(self, service_id, name, base_price, description, complexity_levels):
        self.id = service_id
        self.name = name
        self.base_price = base_price
        self.description = description
        self.complexity_levels = complexity_levels

    def calculate_price(self, complexity, urgency):
        return self.base_price * self.complexity_levels[complexity] * urgency