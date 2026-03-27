import random

def generate_product(i):
    return {
        "id": i,
        "name": f"Product {i}",
        "amazonLink": f"https://www.amazon.com/s?k=product+{i}",
        "price": random.randint(40, 120),

        # AI Metrics
        "demandScore": random.randint(60, 95),
        "competitionScore": random.randint(20, 70),
        "marginScore": random.randint(20, 50),
        "trendScore": random.randint(50, 95),
    }

def generate_products(n=50):
    return [generate_product(i) for i in range(n)]
