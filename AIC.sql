use AIC
go

CREATE TABLE Users(
    User_Id INT PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    DateJoined DATE,
    Number_phone VARCHAR(15),
    Name VARCHAR(100)
);

CREATE TABLE Video (
    Video_Id INT,
    User_Id INT,
    UploadDate DATE,
    Duration TIME,
    Video_Name VARCHAR(255),
    Filepath VARCHAR(255),
    Category VARCHAR(100),
	PRIMARY KEY (Video_Id),
    FOREIGN KEY (User_Id) REFERENCES Users(User_Id)
);

CREATE TABLE History (
    User_Id INT,
    Video_Id INT,
    Date_viewed TIMESTAMP,
    PRIMARY KEY (User_Id, Video_Id, Date_viewed),
    FOREIGN KEY (User_Id) REFERENCES Users(User_Id),
    FOREIGN KEY (Video_Id) REFERENCES Video(Video_Id)
);

CREATE TABLE Event (
    Event_Id INT,
    Video_Id INT,
    Event_Name VARCHAR(255),
    Event_Type VARCHAR(100),
    EventTime TIME,
    Start_Time TIME,
    End_Time TIME,
	PRIMARY KEY(Event_Id,Video_Id),
    FOREIGN KEY (Video_Id) REFERENCES Video(Video_Id)
);


