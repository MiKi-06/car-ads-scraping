from statistics import median
from database import Database

def analyze_market(model="رنو، تندر 90"):
  db = Database()
  try:
    ads = db.get_ads(model)
    prices = [row["price"] for row in ads]
    count = len(prices)
    med_price = median(prices)
    total = sum(prices)
    highest = max(prices)
    lowest = min(prices)
    average = (total // count)
    good_deals = find_good_deals(ads, med_price)
    
    return{
      "count": count,
      "median": med_price,
      "highest": highest,
      "lowest": lowest,
      "average": average
    }, good_deals
  except Exception as e:
    print(e)
  finally:
    db.close()

def find_good_deals(ads, med_price = None, thereshold= 0.9):
  good_deals = []
  if med_price is None:
    prices = [row["price"] for row in ads]
    med_price = median(prices)
  for ad in ads:
    if ad["price"] < (med_price * thereshold):
      good_deals.append(ad)
  
  return good_deals