CREATE TABLE Routes (
	RouteID SERIAL PRIMARY KEY,
	AgencyID INT NOT NULL,
	ShortName VARCHAR(10),
	LongName VARCHAR(200),
	Description TEXT,
	RouteType INT REFERENCES RouteTypes(ID),
	URL TEXT,
	HexColor CHAR(6),
	HexTextColor CHAR(6),
	AgencySortOrder INT
);
