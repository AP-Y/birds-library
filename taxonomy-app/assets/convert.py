#  Code from https://towardsdatascience.com/turn-your-excel-workbook-into-a-sqlite-database-bc6d4fd206aa
# Most of the code is commented out since I don't want to re-create birds.db

import pandas as pd
import sqlite3 # Python package for SQL

# Read the 'eBird taxonomy v2019' table in Excel Sheet eBird_Taxonomy_v2019; save it to birds
# birds = pd.read_excel(
# 	'eBird_Taxonomy_v2019.xlsx',
# 	sheet_name = 'eBird taxonomy v2019',
# 	header = 0
# )

db_conn = sqlite3.connect('birds.db') # Create a birds.db SQL database
# c = db_conn.cursor() # Create a cursor to manipulate that database

# Raw SQL syntax: create birds table in bird.db with column names and datatypes
# c.execute(
# 	"""
# 	CREATE TABLE birds (
# 		Taxon_Order INTEGER,
# 		Category TEXT NOT NULL,
# 		Species_Code TEXT NOT NULL,
# 		Primary_Com_Name TEXT NOT NULL,
# 		Sci_Name TEXT NOT NULL,
# 		Order1 TEXT,
# 		Family TEXT,
# 		Species_Group TEXT,
# 		Report_As TEXT,
# 		PRIMARY KEY(Species_Code)
# 	);
# 	"""
# )

# birds.to_sql('birds', db_conn, if_exists='append', index=False)

print(pd.read_sql('SELECT * FROM birds LIMIT 10', db_conn)) # Print the first 10 rows from the new birds table in birds.db

db_conn.close() # Close the database
