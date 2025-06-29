
import json
import pandas as pd
import pymysql

#db connection
conn = pymysql.connect(
    host='localhost',
    user='db_user',
    password='6equj5_db_user',
    db='home_db',
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = conn.cursor()
#Extract
# Loading JSON file (here we have only one, but i made read for multiple files)
data_paths = ['C:/Users/Acer/Desktop/HomeLLC/data_engineer_assessment/data/fake_property_data.json']
data = []

# Load and concatenate data
for path in data_paths:
    with open(path, 'r') as file:
        data.extend(json.load(file))

df = pd.DataFrame(data)

# Clean function for string fields
def clean_string(val):
    if pd.isna(val) or str(val).strip() == "":
        return "NA"
    return str(val).strip()

# Clean function for numeric fields
def clean_numeric(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

#  Transform
str_columns = [
    'Property_Title', 'Street_Address', 'City', 'State', 'Zip', 'Property_Type',
    'Train', 'Highway', 'HTW', 'Pool', 'Commercial', 'Water', 'Sewage',
    'Parking', 'BasementYesNo', 'Layout', 'Rent_Restricted', 'Final_Reviewer',
    'Reviewed_Status', 'Most_Recent_Status', 'Occupancy', 'Source', 'Selling_Reason',
    'Seller_Retained_Broker'
]

for col in str_columns:
    df[col] = df[col].apply(clean_string)

num_columns = [
    'Tax_Rate', 'Year_Built', 'Neighborhood_Rating', 'School_Average',
    'Net_Yield', 'IRR', 'Latitude', 'Longitude', 'Taxes'
]

for col in num_columns:
    df[col] = df[col].apply(clean_numeric)

# Removing duplicates
df = df.drop_duplicates(subset=[
    "Property_Title", "Street_Address", "City", "State", "Zip", "Latitude", "Longitude"
])


# Load 
for _, row in df.iterrows():
    try:
        # Insert into valuation
        valuation_id = None
        valuations = row.get("Valuation", [])
        for v in valuations:
            cursor.execute("""
                INSERT INTO Valuation (previous_rent, list_price, zestimate, arv,
                    expected_rent, rent_zestimate, low_fmr, high_fmr, redfin_value)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                clean_numeric(v.get("Previous_Rent")),
                clean_numeric(v.get("List_Price")),
                clean_numeric(v.get("Zestimate")),
                clean_numeric(v.get("ARV")),
                clean_numeric(v.get("Expected_Rent")),
                clean_numeric(v.get("Rent_Zestimate")),
                clean_numeric(v.get("Low_FMR")),
                clean_numeric(v.get("High_FMR")),
                clean_numeric(v.get("Redfin_Value"))
            ))
            valuation_id = cursor.lastrowid

        # Insert into rehab
        rehab_id = None
        rehabs = row.get("Rehab", [])
        for r in rehabs:
            cursor.execute("""
                INSERT INTO Rehab (underwriting_rehab, rehab_calculation, paint, flooring_flag,
                    foundation_flag, roof_flag, hvac_flag, kitchen_flag, bathroom_flag,
                    appliances_flag, windows_flag, landscaping_flag, trashout_flag)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                clean_numeric(r.get("Underwriting_Rehab")),
                clean_numeric(r.get("Rehab_Calculation")),
                clean_string(r.get("Paint")),
                clean_string(r.get("Flooring_Flag")),
                clean_string(r.get("Foundation_Flag")),
                clean_string(r.get("Roof_Flag")),
                clean_string(r.get("HVAC_Flag")),
                clean_string(r.get("Kitchen_Flag")),
                clean_string(r.get("Bathroom_Flag")),
                clean_string(r.get("Appliances_Flag")),
                clean_string(r.get("Windows_Flag")),
                clean_string(r.get("Landscaping_Flag")),
                clean_string(r.get("Trashout_Flag"))
            ))
            rehab_id = cursor.lastrowid

        # Insert into HOA
        hoa_id = None
        hoas = row.get("HOA", [])
        for h in hoas:
            cursor.execute("""
                INSERT INTO HOA (hoa, hoa_flag)
                VALUES (%s, %s)
            """, (
                clean_numeric(h.get("HOA")),
                clean_string(h.get("HOA_Flag"))
            ))
            hoa_id = cursor.lastrowid

        # Insert into taxes
        cursor.execute("INSERT INTO Taxes (taxes) VALUES (%s)", (row["Taxes"],))
        taxes_id = cursor.lastrowid

        # Insert into leads
        cursor.execute("""
            INSERT INTO Leads (reviewed_status, most_recent_status, occupancy,
                source, net_yield, irr, selling_reason, seller_retained_broker, final_reviewer)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["Reviewed_Status"], row["Most_Recent_Status"], row["Occupancy"],
            row["Source"], row["Net_Yield"], row["IRR"],
            row["Selling_Reason"], row["Seller_Retained_Broker"], row["Final_Reviewer"]
        ))
        leads_id = cursor.lastrowid

        # Insert into property
        cursor.execute("""
            INSERT INTO property (
                property_title, street_address, city, state, zip, latitude, longitude,
                property_type, train, highway, tax_rate, year_built, htw, pool,
                commercial, water, sewage, parking, basement_yes_no, layout,
                rent_restricted, neighborhood_rating, school_average,
                valuation_id, taxes_id, hoa_id, rehab_id, leads_id
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["Property_Title"], row["Street_Address"], row["City"], row["State"], row["Zip"],
            row["Latitude"], row["Longitude"], row["Property_Type"], row["Train"], row["Highway"],
            row["Tax_Rate"], row["Year_Built"], row["HTW"], row["Pool"], row["Commercial"],
            row["Water"], row["Sewage"], row["Parking"], row["BasementYesNo"], row["Layout"],
            row["Rent_Restricted"], row["Neighborhood_Rating"], row["School_Average"],
            valuation_id, taxes_id, hoa_id, rehab_id, leads_id
        ))

        conn.commit()

    except Exception as e:
        print("Error inserting record:", e)
        conn.rollback()

cursor.close()
conn.close()
