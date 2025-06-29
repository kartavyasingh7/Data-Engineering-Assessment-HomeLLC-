CREATE TABLE property (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_title VARCHAR(255),
    street_address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    zip VARCHAR(20),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    market VARCHAR(100),
    flood VARCHAR(50),
    property_type VARCHAR(100),
    train VARCHAR(100),
    highway VARCHAR(100),
    tax_rate DECIMAL(10,2),
    sqft_basement INT,
    sqft_mu INT,
    sqft_total INT,
    bed INT,
    bath INT,
    htw VARCHAR(100),
    pool VARCHAR(10),
    commercial VARCHAR(10),
    water VARCHAR(100),
    sewage VARCHAR(100),
    year_built INT,
    parking VARCHAR(100),
    basement_yes_no VARCHAR(10),
    layout VARCHAR(100),
    rent_restricted VARCHAR(10),
    neighborhood_rating DECIMAL(3, 2),
    school_average DECIMAL(4, 2),
    subdivision VARCHAR(100),
    
     -- FKs
    leads_id INT,
    valuation_id INT,
    hoa_id INT,
    taxes_id INT,
    rehab_id INT,

    FOREIGN KEY (leads_id) REFERENCES Leads(id),
    FOREIGN KEY (valuation_id) REFERENCES Valuation(id),
    FOREIGN KEY (hoa_id) REFERENCES HOA(id),
    FOREIGN KEY (taxes_id) REFERENCES Taxes(id),
    FOREIGN KEY (rehab_id) REFERENCES Rehab(id)
   
);


CREATE TABLE Leads (
	id INT AUTO_INCREMENT PRIMARY KEY,
	reviewed_status VARCHAR(100),
	most_recent_status VARCHAR(100),
	occupancy VARCHAR(100),
	source VARCHAR(100),
	net_yield DECIMAL(5, 2),
	irr DECIMAL(5, 2),
	selling_reason VARCHAR(100),
	seller_retained_broker VARCHAR(100),
	final_reviewer  VARCHAR(255)
	
);

CREATE TABLE Valuation (
	id INT AUTO_INCREMENT PRIMARY KEY,
	previous_Rent INT,
	list_Price INT,
	zestimate INT,
	ARV INT,
	expected_rent INT,
	Rent_Zestimate INT,
	Low_FMR INT,
	High_FMR INT,
	Redfin_Value INT

);

CREATE TABLE HOA (
	id INT AUTO_INCREMENT PRIMARY KEY,
	hoa INT,
	hoa_flag VARCHAR(10)

);

CREATE TABLE Taxes (
	id INT AUTO_INCREMENT PRIMARY KEY,
	taxes INT

);

CREATE TABLE Rehab (
	id INT AUTO_INCREMENT PRIMARY KEY,
	Underwriting_Rehab INT,
    Rehab_Calculation INT,
    Paint VARCHAR(10),
    Flooring_Flag VARCHAR(10),
    Foundation_Flag VARCHAR(10),
    Roof_Flag VARCHAR(10),
    HVAC_Flag VARCHAR(10),
    Kitchen_Flag VARCHAR(10),
    Bathroom_Flag VARCHAR(10),
    Appliances_Flag VARCHAR(10),
    Windows_Flag VARCHAR(10),
    Landscaping_Flag VARCHAR(10),
    Trashout_Flag VARCHAR(10)

);


