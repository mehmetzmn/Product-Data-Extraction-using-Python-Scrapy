# EPLAN Data Portal Scraper

A robust and scalable web scraper built with Python and Scrapy to extract detailed product information from the EPLAN Data Portal API.

## Features

- **Asynchronous Scraping:** Highly optimized for speed. Reduces extraction time significantly by utilizing Scrapy's async architecture.
- **Dynamic Item Limits:** Can be scaled from the command line without modifying the codebase (e.g., extracting 500 or 5000 items dynamically).
- **Data Sanitization:** Implements custom utility functions to handle API data inconsistencies (handling both `dict` and `list` responses safely) and strips newline characters (`\n`, `\r`) for clean, single-line CSV formatting.
- **Robust Architecture:** Follows Scrapy's best practices using `Items` for rigid data schemas and `utils.py` for modular helper functions.

## Prerequisites

- Python 3.x
- Scrapy
- [uv](https://github.com/astral-sh/uv) (Recommended for fast dependency management)

## Usage

You can run the spider and output the results directly to a CSV file. Use the `-a max_items` argument to define how many products you want to extract.

```bash
uv run scrapy crawl eplan_spider -a max_items=1000 -O extracted_parts.csv
```
