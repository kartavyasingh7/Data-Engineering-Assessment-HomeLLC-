SUBMITTED BY- KARTAVYA SINGH (kartavya.cr07@gmail.com)

HomeLLC
ETL Pipeline for Property Data - Project Documentation



Overview-
This project involves designing and implementing an ETL (Extract, Transform, Load) pipeline to process large scale property listing data in JSON format, clean and normalize it, and load it into a structured MySQL database using a normalized schema.


Objective-

To convert raw, nested, and inconsistent JSON property data into clean, deduplicated, and normalized relational tables that preserve relationships using foreign keys, enabling scalable querying and analysis.

Tech Stack

Language: Python 3.10

Libraries: pandas, json, pymysql

Database: MySQL 

Tools: VS Code, DBeaver, Docker



Schema Design=

The database consists of the following normalized tables:

1. property

Central table containing core attributes of a property along with foreign keys.

2. leads

Stores review and status metadata.

3. valuation

Contains financial estimates like List Price, ARV, Zestimate, FMR values, etc.

4. rehab

Captures detailed rehab metrics and boolean flags.

5. hoa

Stores HOA related details like fees and flags.

6. taxes

Stores tax values for properties.

Each property record links to one entry from each of the related tables using foreign keys: leads_id, valuation_id, rehab_id, hoa_id, taxes_id.



ETL Process:

✅ Extraction-

JSON data was loaded using Python with memory efficient streaming.



✅ Transformation-

Used pandas for dataframe based transformations.

Handled deeply nested fields such as valuation, hoa, and rehab.

Cleaned string fields:

Replaced empty strings ("") or whitespace-only fields with "NA".

Converted invalid numeric/null fields to SQL NULL.

Removed duplicates across all records.



✅ Loading-

Used pymysql to connect to MySQL.

Inserted records table by table, ensuring foreign key constraints were respected.

Batched inserts and committed periodically for performance.



Error Handling-

All insert operations were wrapped in try/except blocks.

Any insertion failure rolled back the transaction for that record.

Detailed error logs printed to console.



Results-

All records were cleaned, deduplicated, and loaded into MySQL.

The relational structure allows flexible joins and querying.

NULLs and NAs are standardized, enabling clean analytics.



How to Run-

Make sure MySQL is running and schema is created using the provided schema.sql.

Update DB credentials in final_etl_script.py.

Place all JSON files in a data/ folder.

Run:
bash python etl.py


