CREATE TABLE StopTimes (
	TripID INT NOT NULL REFERENCES Trips(TripID),
	ArrivalTime TIME NOT NULL, --should use tz?
	DepartureTime TIME NOT NULL,
	StopID INT NOT NULL REFERENCES Stops(StopID),
	StopSequence INT NOT NULL,
	StopHeadsign VARCHAR(200) NULL,
	PickupType SMALLINT DEFAULT 0,
	DropOffType SMALLINT DEFAULT 0,
	TimePoint BIT DEFAULT CAST(1 AS BIT)
);
