import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('scraped_data.db')
cursor = conn.cursor()

# Enable foreign key support
cursor.execute("PRAGMA foreign_keys = ON;")

# Create the ScrapeRuns table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ScrapeRuns (
    ScrapeID INTEGER PRIMARY KEY AUTOINCREMENT,
    ScrapeDate DATE NOT NULL
);
""")

# Create the Sections table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Sections (
    SectionID INTEGER PRIMARY KEY AUTOINCREMENT,
    SectionName TEXT NOT NULL, 
    StoreName TEXT NOT NULL,
    UNIQUE (SectionName, StoreName)
);
""")

# Create the Products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    ProductID INTEGER PRIMARY KEY,
    SectionID INTEGER NOT NULL,
    ProductName TEXT NOT NULL,
    FOREIGN KEY (SectionID) REFERENCES Sections(SectionID)
);
""")

# Create the ProductPrices table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ProductPrices (
    ProductPriceID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductID INTEGER NOT NULL,
    ScrapeID INTEGER NOT NULL,
    ProductPrice TEXT,
    ProductDiscount TEXT,
    ProductDiscountStart DATE,
    ProductDiscountEnd DATE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
    FOREIGN KEY (ScrapeID) REFERENCES ScrapeRuns(ScrapeID)
);
""")

# Create the IndicatorCategories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS IndicatorCategories (
    IndicatorCategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    IndicatorCategoryName TEXT NOT NULL UNIQUE
);
""")

# Create the Indicators table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Indicators (
    IndicatorID INTEGER PRIMARY KEY AUTOINCREMENT,
    IndicatorCategoryID INTEGER NOT NULL,
    IndicatorName TEXT NOT NULL,
    IndicatorUnit TEXT,
    FOREIGN KEY (IndicatorCategoryID) REFERENCES IndicatorCategories(IndicatorCategoryID)
);
""")

# Create the IndicatorValues table
cursor.execute("""
CREATE TABLE IF NOT EXISTS IndicatorValues (
    IndicatorValueID INTEGER PRIMARY KEY AUTOINCREMENT,
    IndicatorID INTEGER NOT NULL,
    ScrapeID INTEGER NOT NULL,
    IndicatorDate DATE NOT NULL,
    IndicatorLatest INTEGER,
    IndicatorPrevious INTEGER,
    FOREIGN KEY (IndicatorID) REFERENCES Indicators(IndicatorID),
    FOREIGN KEY (ScrapeID) REFERENCES ScrapeRuns(ScrapeID)
);
""")

# (Removed unused auxiliary table in prior refactor)

# Commit the changes and close the connection
conn.commit()
conn.close()


# conn = sqlite3.connect('scraped_data.db')
# cursor = conn.cursor()

# # Enable foreign key support
# cursor.execute("PRAGMA foreign_keys = ON;")


# ###Esselunga section names
# sections = [
#     "FruttaVerdura",
#     "SpesaBio",
#     "PesceSushi",
#     "Carne",
#     "LatticiniSalumiFormaggi",
#     "AlimentiVegetali",
#     "PanePasticceria",
#     "GastronomiaPiattiPronti",
#     "ColazioneMerende",
#     "PatatineDolciumi",
#     "ConfezionatiAlimentari",
#     "SurgelatiGelati",
#     "MondoBimbi",
#     "AcquaBibiteBirra",
#     "ViniLiquori",
#     "IgieneCuraPersona",
#     "IntegratoriSanitari",
#     "CuraCasaDetersivi",
#     "TempoLiberoOutdoor",
#     "AmiciAnimali",
#     "CancelleriaPartyGiocattoli",
#     "MultimediaCarteRicariche"
# ]


# for section_name in sections:
#     cursor.execute("""
#         INSERT OR IGNORE INTO Sections (SectionName)
#         VALUES (?)
#     """, (section_name,))

# indicator_categories = ['GDP', 'Labour', 'Prices', 'Trade', 'Government', 'Business', 'Consumer', 'Housing', 'Energy', 'Health']


# for category_name in indicator_categories:
#     cursor.execute("""
#         INSERT OR IGNORE INTO IndicatorCategories (IndicatorCategoryName)
#         VALUES (?)
#     """, (category_name,))

# conn.commit()
# conn.close()    
