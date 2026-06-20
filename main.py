import argparse
from scraper.database import Database
from scraper.excel_exporter import Excelexporter
from scraper.scraper import Scraper
from analysis.analysis import Analyzer
from reporter.market_report import Reporter
def handle_scrape(args):
  try:
    db = Database()
    ex = Excelexporter()
    scraper = Scraper(args.min, args.max, db, ex)
    scraper.scrape()
  except Exception as e:
    print(e)
  finally:
    db.close()
    ex.close()

def handle_analyze(args):
  try:
    db = Database()
    analyzer = Analyzer(db)
    result = analyzer.analyze_market(args.model)
    print(result)
  except Exception as e:
    print(e)
  finally:
    db.close()

def handle_report(args):
  try:
    db = Database()
    analyzer = Analyzer(db)
    reporter = Reporter(analyzer)
    reporter.get_report(args.model)
  except Exception as e:
    print(e)
  finally:
    db.close()


def main():
  parser = argparse.ArgumentParser()
  subparser = parser.add_subparsers(dest="command")

  # scrape
  scrape_parser = subparser.add_parser("scrape",
                      help="Scrapes ads")
  scrape_parser.add_argument("--min",
                      type=int,
                      default=0,
                      help="Minimum price for ads")
  scrape_parser.add_argument("--max",
                      type=int,
                      default=100_000_000_000,
                      help="Maximum price for ads")

  #analyze
  analyze_parser = subparser.add_parser("analyze")
  analyze_parser.add_argument("--model",
                              required=True)

  #report
  report_parser = subparser.add_parser("report")
  report_parser.add_argument("--model",
                              required=True)
  
  scrape_parser.set_defaults(func=handle_scrape)
  analyze_parser.set_defaults(func=handle_analyze)
  report_parser.set_defaults(func=handle_report)

  args = parser.parse_args()

  if hasattr(args, "func"):
      args.func(args)
  else:
      parser.print_help()

if __name__ == "__main__":
  main()

