from statistics import median
from .statistics_utils import remove_outliers, get_score

class Analyzer:
  def __init__(self, db):
    self.db = db

  def analyze_market(self, model="رنو، تندر 90"):
    try:
      ads = self.db.fetch_ads(model)
      if not ads:
        print("no data")
        return{
        "statistics": {
                      "model": model,
                      "count": 0,
                      "median": 0,
                      "highest": 0,
                      "lowest": 0,
                      "average": 0
                      },
        "rated_deals": []
      } 
      prices = [row["price"] for row in ads]
      # removes the outlier prices
      prices = remove_outliers(prices)
      count = len(prices)
      med_price = median(prices)
      total = sum(prices)
      highest = max(prices)
      lowest = min(prices)
      average = (total // count)
      rated_deals = self.get_rate_ads(ads, med_price)
      return{
        "statistics": {
                      "model": model,
                      "count": count,
                      "median": med_price,
                      "highest": highest,
                      "lowest": lowest,
                      "average": average
                      },
        "rated_deals": rated_deals
      } 
    except Exception as e:
      raise e

  def get_rate_ads(self, ads, med_price = None):
    rated_ads = []
    if med_price is None:
      prices = [row["price"] for row in ads]
      med_price = median(prices)
    for ad in ads:
      score = get_score(ad, med_price)
      ad = dict(ad)
      ad["score"] = score["score"]
      print(ad["score"])
      ad["diff_percent"] = score["percent"]
      print(ad["diff_percent"])
      rated_ads.append(ad)
  
    self.db.insert_into("rated_ads", rated_ads)
    return rated_ads
  

  def market_score(self, model):
    pass