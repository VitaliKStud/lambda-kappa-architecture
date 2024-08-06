import random
from datetime import datetime

class SnackAutomat:

    def __init__(self, snack_automat_id):
        self.snacks = {"position_1": "apple", "position_2": "banana",
                       "position_3": "orange", "position_4": "blueberries",
                       "position_5": "snickers", "position_6": "mars",
                       "position_7": "twix", "position_8": "milkyway"}
        self.snack_automat_id = snack_automat_id
        self.prices = {"apple": 1, "banana": 1, "orange": 1, "blueberries": 2,
                       "snickers": 3, "mars": 3, "twix": 3, "milkyway": 3}

    def get_price(self, snack):
        return self.prices[snack]


    def get_random_item(self):
        return random.choice(list(self.snacks.keys()))

    def get_random_number_of_items(self):
        choices = [i for i in range(1, 9)]
        weights = [i for i in range(8, 0, -1)]
        random_number = random.choices(choices, weights=weights, k=1)[0]
        return random_number

    def get_random_customer(self):
        return random.randint(0, 200)

    def get_bought_items(self):
        customer = self.get_random_customer()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for i in range(1, self.get_random_number_of_items() + 1):
            item = self.get_random_item()
            snack = self.snacks[item]
            price = self.get_price(snack)
            if item in ["position_1", "position_2", "position_3", "position_4"]:
                healthy = "healthy"
            else:
                healthy = "not_healthy"
            yield {"item": snack, # snack is correct
                   "customer_id": customer,
                   "healthy_food": healthy,
                   "price": price,
                   "snack_automat_id": self.snack_automat_id,
                   "timestamp": timestamp,
                   "ones": 1}