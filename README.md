# Car Ads Scraping & Market Analysis
*This project was built as a learning project to practice web scraping, database design, and data analysis with Python.‎*

A Python project for collecting used car advertisements, storing them in a SQLite database, and analyzing market prices.

## Features

- Scrape car advertisements using Selenium
- Store data in SQLite
- Prevent duplicate records using unique links
- Normalize Persian dates
- Remove price outliers
- Calculate market statistics
  - Median price
  - Average price
  - Minimum and maximum prices
- Find potentially underpriced ("good deal") advertisements
- Analyze advertisements by car model

## Tech Stack

- Python
- Selenium
- SQLite
- NumPy
- Regular Expressions
- jdatetime

## Project Structure

```
car-ads-scraping/
│
├── scraper.py
├── database.py
├── analysis.py
├── statistics_utils.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## Current Status

This project is currently paused while I focus on learning newer technologies and building more advanced projects.

The existing implementation provides a complete workflow for:

1. Collecting advertisements
2. Saving them into a database
3. Cleaning and processing data
4. Performing basic market analysis

Future improvements may include:

- REST API
- Docker support
- Scheduled scraping
- Multi-source data collection
- Machine Learning price prediction
- Interactive web dashboard

## Example Analysis

The project can calculate:

- Market median price
- Average price
- Price range
- Outlier removal
- Good deal detection based on configurable thresholds

## Installation

```bash
git clone https://github.com/your_username/car-ads-scraping.git

cd car-ads-scraping

pip install -r requirements.txt
```

## Future Plans

Although development is currently on hold, the project is planned to evolve into a more complete used-car market analysis platform.

## License

MIT License
