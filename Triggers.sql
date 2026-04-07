--This trigger checks if the event exists in the Event table before inserting a new medal record.
DELIMITER //

CREATE TRIGGER BeforeMedalInsert
BEFORE INSERT ON Medal
FOR EACH ROW
BEGIN
    DECLARE event_exists INT;

    SELECT COUNT(*) INTO event_exists
    FROM Event
    WHERE event_name = NEW.event_name;

    IF event_exists = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Event does not exist.';
    END IF;
END //

DELIMITER ;

--This trigger will prevent the insertion of duplicate athletes with the same athleteCode.
DELIMITER //

CREATE TRIGGER PreventDuplicateAthlete
BEFORE INSERT ON Athlete
FOR EACH ROW
BEGIN
    DECLARE athlete_exists INT;
    
    SELECT COUNT(*) INTO athlete_exists 
    FROM Athlete 
    WHERE athleteCode = NEW.athleteCode;

    IF athlete_exists > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Athlete with this code already exists';
    END IF;
END //

DELIMITER ;
