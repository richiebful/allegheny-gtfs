DROP TABLE IF EXISTS Agencies;
DROP TABLE IF EXISTS Stops;
DROP TABLE IF EXISTS Trips;
DROP TABLE IF EXISTS FareRules;
DROP TABLE IF EXISTS FareSpec;
DROP TABLE IF EXISTS StopTimes;
DROP TABLE IF EXISTS ServiceCalendar;
DROP TABLE IF EXISTS ServiceExceptions;


CREATE TABLE Agencies(
	AgencyID SERIAL PRIMARY KEY,
	ShortName VARCHAR(50),
	LongName VARCHAR(200)
);

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
	StopTimezone INT, --need actual datatype
	WheelchairAccessID SMALLINT
);

CREATE TABLE Routes (
	RouteID SERIAL PRIMARY KEY,
	AgencyID INT NOT NULL,
	ShortName VARCHAR(10),
	LongName VARCHAR(200),
	Description TEXT,
	RouteType CHAR,
	URL TEXT,
	HexColor CHAR(6),
	HexTextColor CHAR(6),
	AgencySortOrder INT
);

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

CREATE TABLE FareSpec (
	FareID SERIAL PRIMARY KEY,
	Price MONEY NOT NULL,
	CurrencyType CHAR(3) NOT NULL,
	PaymentMethod BIT NOT NULL,
	Transfers INT NOT NULL, --transform NULL to -1
	AgencyID INT,
	TransferDuration INT
);

CREATE TABLE FareRules (
	FareID INT NOT NULL REFERENCES FareSpec(FareID),
	RouteID INT REFERENCES Routes(RouteID),
	OriginID INT,
	DestinationID INT,
	ContainsID INT
);

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

CREATE TABLE ServiceCalendar (
	ServiceID INT NOT NULL,
	Monday BIT NOT NULL,
	Tuesday BIT NOT NULL,
	Wednesday BIT NOT NULL,
	Thursday BIT NOT NULL,
	Friday BIT NOT NULL,
	Saturday BIT NOT NULL,
	Sunday BIT NOT NULL,
	StartDate DATE NOT NULL,
	EndDate DATE NOT NULL
);

CREATE TABLE ServiceExceptions (
	ServiceID INT NOT NULL,
	ServiceDate DATE NOT NULL,
	ExceptionType SMALLINT NOT NULL
);
