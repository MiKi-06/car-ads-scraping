import argparse
from scraper.database import Database
from scraper.excel_exporter import Excelexporter
from scraper.scraper import Scraper
def handle_scrape(args):
  db = Database()
  ex = Excelexporter()
  scraper = Scraper(args.min, args.max, db, ex)
  scraper.scrape()

  db.close()
  ex.close()

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

  args = parser.parse_args()

  if args.command == "scrape":
    handle_scrape(args)


if __name__ == "__main__":
  main()

