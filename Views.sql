DELIMITER //

CREATE VIEW AUSathletes AS
SELECT *
FROM Athlete
WHERE country_code = 'AUS';  

DELIMITER ;
