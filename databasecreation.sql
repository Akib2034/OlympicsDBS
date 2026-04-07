-- Drop the Olympics Database if it exists
DROP DATABASE IF EXISTS OlympicsDatabase_21341382;

-- Create the Olympics Database
CREATE DATABASE OlympicsDatabase_21341382;


-- Select the newly created database

USE OlympicsDatabase_21341382;

-- Create the Country table

CREATE TABLE IF NOT EXISTS Country (
    country_code CHAR(3) PRIMARY KEY,  -- The 3-character country code .
    country_name VARCHAR(100) NOT NULL -- The full name of the country.
);

-- Create the Athlete table

CREATE TABLE IF NOT EXISTS Athlete (
    athleteCode VARCHAR(100) PRIMARY KEY, -- Unique identifier for each athlete.
    name VARCHAR(100) NOT NULL,        -- Athlete's name.
    gender CHAR(1) ,		       -- Gender of the athlete .
    country_code CHAR(3),              -- Foreign key reference to Country table.
    event_name VARCHAR(300),	       -- Foreign key reference to Event.
    birthdate DATE,                    -- Athlete's date of birth.
    coach VARCHAR(1000),                -- Name of the athlete's coach .
    FOREIGN KEY (country_code)
    REFERENCES Country(country_code)   -- Ensures that the country_code exists in the Country table.
);

-- Create the Event table

CREATE TABLE IF NOT EXISTS Event (
    event_name VARCHAR(300),              -- The name of the event (e.g., "100m Sprint").
    sport VARCHAR(50) NOT NULL,           -- Name of the sport (e.g., "Athletics").
    sport_code VARCHAR(10),                -- A short code representing the sport (e.g., "ATH").

    PRIMARY KEY (event_name, sport)       -- Composite primary key
);


-- Create the Medal table

CREATE TABLE IF NOT EXISTS Medal (
    medal_type VARCHAR(20),  		      -- Type of medal awarded.
    medal_code INT ,                          -- Unique identifier for each medal.
    
    athleteName VARCHAR(100) NOT NULL,        -- The name of the athlete .
    gender CHAR(1) NOT NULL,                  -- Gender of the athlete .
    discipline VARCHAR(50) NOT NULL,          -- The discipline of the event .
    event_name VARCHAR(100) NOT NULL,         -- Foreign key reference to the Event where the medal was won.
    code VARCHAR(100) NOT NULL,               -- Can represent either an athlete's code or a team's code.
    country_code CHAR(3) NOT NULL,            -- Foreign key reference to the country of the athlete/team.
    PRIMARY KEY (medal_code,code,event_name),
    FOREIGN KEY (event_name) 
    REFERENCES Event(event_name),              -- Ensures the event exists in the Event table.
    
    FOREIGN KEY (country_code) 
    REFERENCES Country(country_code)            -- Ensures the country exists in the Country table.
);


-- Create the Venues table

CREATE TABLE  IF NOT EXISTS Venues (
    venue VARCHAR(50) PRIMARY KEY,     -- Unique name or identifier for the venue.
    sports VARCHAR(100),                 -- The sports held at the venue.
    date_start DATE,                    -- Start date of the event at this venue.
    date_end DATE                       -- End date of the event at this venue.
);

-- Create the Athletics table

CREATE TABLE  IF NOT EXISTS Athletics (
    event_name VARCHAR(100) NOT NULL,            -- Foreign key reference to Event.
    stage VARCHAR(50),                            -- The stage of the event (e.g., Final, Heats).
    gender CHAR(1),                              -- The gender category for the event.
    venue VARCHAR(50) NOT NULL,                 -- Foreign key reference to Venue.
    athleteCode VARCHAR(100) NOT NULL,                    -- Foreign key reference to Athlete.
    athleteName VARCHAR(100) NOT NULL,           -- The name of the athlete participating in the event.

    country_code CHAR(3) NOT NULL,               -- Foreign key reference to the athlete's country.
    position INT NULL,                                     -- Athlete's rank or position in the event.
    result DECIMAL(10, 2),                        -- Athlete's performance result (e.g., time, distance).
    result_type VARCHAR(50),                      -- The type of result (e.g., time, distance).
    
    
    FOREIGN KEY (event_name) 
    REFERENCES Event(event_name),                 -- Ensures the event exists in the Event table.
                      
    FOREIGN KEY (country_code) 
    REFERENCES Country(country_code)               -- Ensures the country exists in the Country table.
);



