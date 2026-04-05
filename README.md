# mercadolivre-scraper

An end-to-end data pipeline that extracts notebook listings from Mercado Livre, transforms and loads the data into a SQLite database, and visualizes insights through an interactive Streamlit dashboard.

## Pipeline Overview

```
Extract (Scrapy) → Transform (Pandas) → Load (SQLite) → Visualize (Streamlit)
```

## Tech Stack

| Layer | Tool |
|---|---|
| Extraction | Scrapy |
| Transformation | Pandas |
| Storage | SQLite |
| Visualization | Streamlit + Plotly |

## Project Structure

```
mercadolivre-scraper/
├── src/
│   ├── extraction/          # Scrapy project
│   │   ├── spiders/
│   │   │   └── notebook.py  # Spider targeting Mercado Livre notebook listings
│   │   ├── settings.py
│   │   └── items.py
│   ├── transform-load/
│   │   └── main.py          # Data cleaning, transformation and SQLite load
│   └── dashboard/
│       └── app.py           # Streamlit dashboard
├── data/
│   ├── data.json            # Raw scraped data
│   └── mercadolivre.db      # SQLite database
└── requirements.txt
```

## Features

- Scrapes notebook listings across 10 pages of Mercado Livre search results
- Extracts seller, product name, old price, new price, and average review score
- Cleans and transforms raw data: null handling, type conversion, duplicate removal
- Calculates discount percentage per product
- Filters outliers by price range
- Interactive dashboard with seller analysis, price distribution, discount vs. price scatter, and best deals table

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/v-machado-dev/mercadolivre-scraper.git
cd mercadolivre-scraper
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the spider**
```bash
cd src/extraction
scrapy crawl notebook -o ../../data/data.json
```

**5. Run the transform and load stage**
```bash
cd ../..
python src/transform-load/main.py
```

**6. Launch the dashboard**
```bash
streamlit run src/dashboard/app.py
```

## Dashboard Preview

The dashboard includes:
- KPI cards: total listings, average discount, average price, average rating
- Listings by seller (bar chart)
- Price distribution (histogram)
- Discount % vs. current price colored by rating (scatter plot)
- Average rating by seller (bar chart)
- Best deals table: highest discount among top-rated products

## Notes

- `ROBOTSTXT_OBEY` is set to `False` in `settings.py` to allow scraping of paginated results
- A custom `USER_AGENT` is configured to mimic a real browser request
- `DOWNLOAD_DELAY` is set to 1 second to avoid overloading the server

## Author

[v-machado-dev](https://github.com/v-machado-dev)
