import numpy as np

def remove_outliers(prices):
  prices = np.array(prices)
  q1 = np.percentile(prices, 25)
  q3 = np.percentile(prices, 75)

  iqr = (q3 - q1)

  lower = (q1 - (1.5 * iqr))
  upper = (q3 + (1.5 * iqr))
  
  filtered = prices[(prices >= lower) & (prices <= upper)]
  return filtered