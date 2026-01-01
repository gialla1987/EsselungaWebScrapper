# EsselungaWebScrapper AI Coding Instructions

## Project Architecture

This is a **web scraping and data pipeline project** that collects Italian grocery store pricing and economic indicators into SQLite. The system has three main flows:

### Core Data Flow
1. **Product Scraping** (`EsselungaScrapper.py`): Scrapes Esselunga grocery categories using Selenium/BeautifulSoup
2. **Auxiliary Data** (`AuxiliaryData.py`): Collects economic indicators from Trading Economics
3. **Database Insertion** (`InsertTodb.py`): Writes all data to `scraped_data.db` using type-based routing
4. **Orchestration** (`EsselungaMain.py`): Entry point that creates scrape run records and coordinates all components

### Data Model
- **`Prod` class** (`models.py`): Represents a product category with parallel lists for IDs, names, prices, and discount metadata
- **`Indicators` class** (`models.py`): Represents economic category data with parallel lists for name, latest/previous values, units, dates
- **Database schema** (`Createdb.py`): Normalized SQLite with foreign keys across Sections→Products→ProductPrices and IndicatorCategories→Indicators→IndicatorValues

## Critical Implementation Patterns

### Web Scraping with Selenium
- **Infinite scroll handling** (`EsselungaScrapper.py:Main`): Poll page height 3 times with 0.5s-3s delays before declaring scroll complete
- **Element extraction**: Use `product.find('div', class_='product')` pattern with class-based selectors, fallback to `get_text(strip=True)` for text content
- **Promotion parsing** (`FindPromotions`): Regex extraction from `el-tooltip` attributes to parse discount descriptions and dates (format: `"text (dal dd/mm/yyyy al dd/mm/yyyy)"`)
- **Hardcoded ChromeDriver path**: `'C:/Users/leona/Desktop/ML stuff/chromedriver-win64/chromedriver.exe'` must be updated when deploying (extract to config)

### Data Insertion Pattern
The `Insert()` function in `InsertTodb.py` uses **type-based routing** with `isinstance()` checks:
```python
if isinstance(Info, Prod):
    InsertProds(Info, ScrapeID)  # Batch inserts products + prices
elif isinstance(Info, Indicators):
    InsertIndices(Info, ScrapeID)  # Scrape-run aggregated indicators
```
Always pass objects through `Insert()` wrapper rather than calling specific functions directly.

### Data Collection Pattern
- **22 product categories** hardcoded in `EsselungaMain.py` as `Prod` objects
- **11 economic categories** scraped from Trading Economics via button clicks (e.g., `#gdp`, `#labour`)
- Each scrape run gets a unique `ScrapeID` (inserted first to maintain referential integrity)
- All data tied to single date (`scrape_date = date.today()`)

## Common Tasks & Workflows

### Adding a New Product Category
1. Create new `Prod` object in `EsselungaMain.py` with section name and URL
2. Append to `objects_list` 
3. Loop passes through `EsselungaScrapper.Main()` which populates parallel lists

### Debugging Scraper Failures
- Check hardcoded ChromeDriver path exists
- Verify Esselunga HTML structure hasn't changed (CSS selectors: `.product`, `.product-label-price-unit`, `.product-promotional`)
- Test scroll completion logic: browser may need more wait time if network is slow

### Extending with New Data Source
1. Create data collection function in `AuxiliaryData.py` that returns `Prod` or `Indicators`
2. Call result through `InsertTodb.Insert(data, scrape_id)` 
3. Update database schema in `Createdb.py` if new tables needed

## Dependencies & Configuration
- **Selenium**: WebDriver with Chrome options for no-first-run, no-browser-check, no-search-screen
- **BeautifulSoup**: HTML parsing with lxml parser
- **SQLite3**: Foreign keys enabled globally (`PRAGMA foreign_keys = ON`)
- **Trading Economics**: Browser-scraped via Selenium (uses CSS selectors for tab navigation)

## Known Issues & TODOs
- ChromeDriver path hardcoded to user's machine—needs environment config
- OpenAI API key reference in `AuxiliaryData.py` marked as TODO before GitHub publication
- Multiple commented-out legacy methods in `EsselungaMainV2Classes.py` and scraper examples (can be removed)
- `FindStrikes()`, `FindDemand()`, `FindTrends()` functions stubbed but not implemented
