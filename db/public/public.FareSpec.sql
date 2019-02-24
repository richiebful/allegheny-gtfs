CREATE TABLE FareSpec (
	FareID SERIAL PRIMARY KEY,
	Price MONEY NOT NULL,
	CurrencyType CHAR(3) NOT NULL,
	PaymentMethod BIT NOT NULL,
	Transfers INT NOT NULL, --transform NULL to -1
	AgencyID INT,
	TransferDuration INT
);
