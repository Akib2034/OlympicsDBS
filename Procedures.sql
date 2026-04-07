CREATE PROCEDURE AddAthlete (
     p_athleteCode INT,
     p_name VARCHAR(100),
     p_gender CHAR(1),
     p_country_code CHAR(3),
     p_event_name VARCHAR(100),
     p_birthdate DATE,
     p_coach VARCHAR(100)
)
COMMENT 'Adds a new athlete to the Athlete table without checking the event name.'

    INSERT INTO Athlete(athleteCode, name, gender, country_code, event_name, birthdate, coach)
    VALUES (p_athleteCode, p_name, p_gender, p_country_code, p_event_name, p_birthdate, p_coach);


CREATE PROCEDURE GetAthleteMedalCount (
     p_athleteName VARCHAR(100)
)
COMMENT 'Retrieves the total count of medals won by a specific athlete'

    SELECT COUNT(*) AS total_medals
    FROM Medal
    WHERE LOWER(athleteName) = LOWER(p_athleteName);

CREATE PROCEDURE UpdateAthlete (
    p_athleteCode INT,
    p_name VARCHAR(100),
    p_gender CHAR(1),
    p_country_code CHAR(3),
    p_event_name VARCHAR(100),
    p_birthdate DATE,
    p_coach VARCHAR(100)
)
COMMENT 'Updates the details of an existing athlete based on athlete code.'

    UPDATE Athlete
    SET
        name = p_name,
        gender = p_gender,
        country_code = p_country_code,
        event_name = p_event_name,
        birthdate = p_birthdate,
        coach = p_coach
    WHERE athleteCode = p_athleteCode;


CREATE PROCEDURE DeleteAthlete (
    p_athleteCode INT
)
COMMENT 'Deletes an athlete from the Athlete table based on athlete code.'

    DELETE FROM Athlete
    WHERE athleteCode = p_athleteCode;


