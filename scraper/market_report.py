from analysis import Analyzer
from database import Database
class Reporter:
  def __init__(self):
    db = Database()
    self.analyzer = Analyzer(db)

  def get_report(self, model= "رنو، تندر 90"):
    report = self.analyzer.analyze_market(model)
    print("================================")
    print("Model: \n", report['statistics']['model'])
    print("\nAds count: \n", report['statistics']['count'])
    print("\nMedian Price: \n", report['statistics']['median'])
    print("\nAverage Price: \n", report['statistics']['average'])
    print("\nHighest: \n", report['statistics']['highest'])
    print("\nLowest: \n", report['statistics']['lowest'])
    print("\nGood Deals: \n", len(report['good_deals']))
    print("================================")


