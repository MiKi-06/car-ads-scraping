
class Reporter:
  def __init__(self, analyzer):
    self.analyzer = analyzer

  def get_report(self, model= "رنو، تندر 90"):
    report = self.analyzer.analyze_market(model)
    if not report:
      print("no data to report")
      return
    print("================================")
    print("Model: \n", report['statistics']['model'])
    print("\nAds count: \n", report['statistics']['count'])
    print("\nMedian Price: \n", report['statistics']['median'])
    print("\nAverage Price: \n", report['statistics']['average'])
    print("\nHighest: \n", report['statistics']['highest'])
    print("\nLowest: \n", report['statistics']['lowest'])
    print("\nGood Deals: \n", len(report['rated_deals']))
    print("================================")


