from statistics import median
from database import Database

def analyze_market(model="رنو، تندر 90"):
  db = Database()
  try:
    ads = db.get_ads(model)
    prices = [row[3] for row in ads]
    count = len(prices)
    med_price = median(prices)
    total = sum(prices)
    highest = max(prices)
    lowest = min(prices)
    average = (total // count)

    print({
      "count": count,
      "median": med_price,
      "highest": highest,
      "lowest": lowest,
      "average": average
    })
    find_good_deals(ads, med_price, model)
  except Exception as e:
    print(e)
  finally:
    db.close()

def find_good_deals(ads, med_price = None, model="رنو، تندر 90"):
  good_deals = []
  if not med_price:
    prices = [row[3] for row in ads]
    med_price = median(prices)
  for ad in ads:
    if ad[3] < (med_price * 0.9):
      good_deals.append(ad)
  print(good_deals)