CREATE TABLE Stops(
	StopID SERIAL PRIMARY KEY,
	Code VARCHAR(20),
	Name VARCHAR(200),
	Description TEXT,
	Location GEOMETRY,
	ZoneID INT,
	StopURL TEXT,
	LocationType SMALLINT,
	ParentStation INT REFERENCES Stops(StopID),
	StopTimezone INT,
	WheelchairAccessID SMALLINT
);
