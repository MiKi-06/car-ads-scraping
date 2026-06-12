from statistics import median
from database import Database

class Analyzer():
  def __init__(self):
    self.db = Database()

  def analyze_market(self, model="رنو، تندر 90"):
    try:
      ads = self.db.get_ads(model)
      prices = [row["price"] for row in ads]
      count = len(prices)
      med_price = median(prices)
      total = sum(prices)
      highest = max(prices)
      lowest = min(prices)
      average = (total // count)
      good_deals = self.find_good_deals(ads, med_price)
      
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
      self.db.close()

  def find_good_deals(self, ads, med_price = None, threshold= 0.9):
    good_deals = []
    if med_price is None:
      prices = [row["price"] for row in ads]
      med_price = median(prices)
    for ad in ads:
      if ad["price"] < (med_price * threshold):
        good_deals.append(ad)
    self.db.insert_into("good_deals", good_deals)
    return good_deals