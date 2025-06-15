from datetime import datetime

class Order:
    def __init__(self, user_id, service, complexity, urgency, details):
        self.user_id = user_id
        self.service = service
        self.complexity = complexity
        self.urgency = urgency
        self.details = details
        self.status = "в обработке"
        self.created_at = datetime.now()