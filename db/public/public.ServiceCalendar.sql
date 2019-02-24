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
