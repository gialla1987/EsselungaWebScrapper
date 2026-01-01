import sqlite3
from datetime import date
from models import Prod, Indicators

def InsertProds(prod, ScrapeID): ###This inserts the theoreticaly Static  names (prods and indicators)
    #print("here2")
    conn = sqlite3.connect('scraped_data.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    section_name = prod.Section
    store_name = prod.StoreName
    # Insert the section if it doesn't exist
    cursor.execute("""
        INSERT OR IGNORE INTO Sections (SectionName, StoreName)
        VALUES (?, ?)
    """, (section_name,store_name,))
    
    # Get the SectionID
    cursor.execute("""
        SELECT SectionID FROM Sections WHERE SectionName = ?
    """, (section_name,))
    section_id = cursor.fetchone()[0]
    
    # Prepare product data for batch insertion
    products_data = []
    product_prices_data = []
    
    num_products = len(prod.ProductsIDs)
    for i in range(num_products):
        product_id = prod.ProductsIDs[i]
        product_name = prod.ProductsNames[i]
        product_price = prod.ProductsPrices[i]
        product_discount = prod.ProductsDiscounts[i]
        discount_start = prod.ProductsDiscountsStart[i]
        discount_end = prod.ProductsDiscountsEnd[i]
        
        # Add to products_data
        products_data.append((product_id, section_id, product_name))
        
        # Add to product_prices_data
        product_prices_data.append((
            product_id,
            ScrapeID,
            product_price,
            product_discount,
            discount_start,
            discount_end
        ))
    #print("here3")
    # Batch insert products
    cursor.executemany("""
        INSERT OR IGNORE INTO Products (ProductID, SectionID, ProductName)
        VALUES (?, ?, ?)
    """, products_data)
    #print("here4")
    # Batch insert product prices
    cursor.executemany("""
        INSERT INTO ProductPrices (
            ProductID, ScrapeID, ProductPrice, ProductDiscount, ProductDiscountStart, ProductDiscountEnd
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, product_prices_data)
    conn.commit()
    conn.close()
    #print("here5")

def InsertIndices(Info, ScrapeID):##This Will insert the non static values (prods and indicators)
    conn = sqlite3.connect('scraped_data.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    category_name = Info.Category

    # Insert the category if it doesn't exist
    cursor.execute("""
        INSERT OR IGNORE INTO IndicatorCategories (IndicatorCategoryName)
        VALUES (?)
    """, (category_name,))

    # Get the IndicatorCategoryID
    cursor.execute("""
        SELECT IndicatorCategoryID FROM IndicatorCategories WHERE IndicatorCategoryName = ?
    """, (category_name,))
    category_id = cursor.fetchone()[0]

    # Prepare data for batch insertion
    indicators_data = []
    indicator_values_data = []

    num_indicators = len(Info.IndicatorName)
    for i in range(num_indicators):
        indicator_name = Info.IndicatorName[i]
        indicator_latest = Info.IndicatorLatest[i]
        indicator_previous = Info.IndicatorPrevious[i]
        indicator_unit = Info.IndicatorUnit[i]
        indicator_date = Info.IndicatorDate[i]

        # Insert the indicator into the Indicators table if it doesn't exist
        cursor.execute("""
            INSERT OR IGNORE INTO Indicators (IndicatorCategoryID, IndicatorName, IndicatorUnit)
            VALUES (?, ?, ?)
        """, (category_id, indicator_name, indicator_unit))

        # Get the IndicatorID
        cursor.execute("""
            SELECT IndicatorID FROM Indicators WHERE IndicatorName = ? AND IndicatorCategoryID = ?
        """, (indicator_name, category_id))
        indicator_id = cursor.fetchone()[0]

        # Prepare data for IndicatorValues
        indicator_values_data.append((
            indicator_id,
            ScrapeID,
            indicator_date,
            indicator_latest,
            indicator_previous
        ))

    # Batch insert indicator values
    cursor.executemany("""
        INSERT INTO IndicatorValues (
            IndicatorID, ScrapeID, IndicatorDate, IndicatorLatest, IndicatorPrevious
        ) VALUES (?, ?, ?, ?, ?)
    """, indicator_values_data)

    # Commit after each category to keep transactions manageable
    conn.commit()
    conn.close()




###Need to pass Products, list of lists. Products prices, list of lists. Indicator names, list of lsits.
###Insert Indicator values, list of lists.


def Insert(Info, ScrapeID):
    #print("here0")
    if isinstance(Info, Prod):
        InsertProds(Info, ScrapeID)
    elif isinstance(Info, Indicators):
        InsertIndices(Info, ScrapeID)
    else:
        print(f"Unknown data type: {type(Info)}")

    # try:
    #     #print("hereA")
    #     test = Info.Section
    #     #print("hereB")
    #     InsertProds(Info, ScrapeID)
    #     #print("here1")
    # except:
    #     try:
    #         test = Info.Category
    #         InsertIndices(Info, ScrapeID)
    #     except:
    #         pass
    
        
    
    


