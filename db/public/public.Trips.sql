CREATE TABLE Trips (
	TripID SERIAL PRIMARY KEY,
	RouteID INT NOT NULL REFERENCES Routes(RouteID),
	ServiceID INT NOT NULL,
	Headsign VARCHAR(200),
	ShortName VARCHAR(100),
	DirectionID BIT,
	BlockID INT,
	Shape PATH,
	WheelchairAccessID SMALLINT,
	BikeAccessID SMALLINT
);
