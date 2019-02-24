CREATE TABLE FareRules (
	FareID INT NOT NULL REFERENCES FareSpec(FareID),
	RouteID INT REFERENCES Routes(RouteID),
	OriginID INT,
	DestinationID INT,
	ContainsID INT
);
