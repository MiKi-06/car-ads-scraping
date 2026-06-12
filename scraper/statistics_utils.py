import numpy as np
from statistics import median
def remove_outliers(prices):
  prices = np.array(prices)
  q1 = np.percentile(prices, 25)
  q3 = np.percentile(prices, 75)

  iqr = (q3 - q1)

  lower = (q1 - (1.5 * iqr))
  upper = (q3 + (1.5 * iqr))
  
  filtered = prices[(prices >= lower) & (prices <= upper)]
  return filtered

def get_score(deal, med_price):
  deal_price = deal["price"]
  difference = med_price - deal_price
  diff_percent = (difference / med_price) * 100
  diff_percent = round(diff_percent, 2)
  if diff_percent <= -11.4:
    score = f"Excellent 🟢 {diff_percent}"
  elif diff_percent >= 18:
    score = f"Overpriced 🔴 {diff_percent}"
  elif -11.4 < diff_percent < 3:
    score = f"Fair Price 🟡 {diff_percent}"
  else:
    score = f"Slightly Expensive 🟠 {diff_percent}"

  return{
    "price": deal_price,
    "marke_price": med_price,
    "percent": diff_percent,
    "score": score
  }


