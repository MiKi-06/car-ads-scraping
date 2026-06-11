from statistics import median
from database import Database

def analyze_market(model="رنو، تندر 90"):
  db = Database()
  try:
    prices = db.get_prices(model)
    count = len(prices)
    med_price = median(prices)
    total = sum(prices)
    highest = max(prices)
    lowest = min(prices)
    average = (total // count)
  except Exception as e:
    print(e)
  finally:
    print({
      "count": count,
      "median": med_price,
      "highest": highest,
      "lowest": lowest,
      "average": average
    })
    db.close()
