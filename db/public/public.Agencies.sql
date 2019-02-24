CREATE TABLE Agencies(
	AgencyID SERIAL PRIMARY KEY,
	ShortName VARCHAR(50),
	LongName VARCHAR(200),
	URL TEXT,
	AgencyTimezone VARCHAR(50)
);
