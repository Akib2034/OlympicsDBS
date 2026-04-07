-- Question: List all event names for the sport "Athletics".
SELECT event_name
FROM Event
WHERE sport = 'Athletics';

-- Question: Find out how many athletes are representing each country.
SELECT country_code, COUNT(*) AS athlete_count 
FROM Athlete 
GROUP BY country_code;

-- Question: Count the number of medals each country has won.
SELECT Country.country_name, COUNT(Medal.medal_code) AS medal_count
FROM Medal
JOIN Country ON Medal.country_code = Country.country_code
GROUP BY Country.country_name
ORDER BY medal_count DESC;

-- Question: List countries that have won at least 3 medals.
SELECT Country.country_name, COUNT(Medal.medal_code) AS medal_count
FROM Medal
JOIN Country ON Medal.country_code = Country.country_code
GROUP BY Country.country_name
HAVING medal_count >= 3;

-- Question: Find athletes whose age is less than 22.
SELECT athleteCode, name, birthdate, 
       TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) AS age
FROM Athlete
WHERE TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) < 22;

-- Question: Count the number of athletes from Australia.
SELECT COUNT(*) AS total_athletes
FROM Athlete
WHERE country_code = 'AUS';

-- Question: Count how many medals were won by athletes from Australia (AUS).
SELECT COUNT(*) AS total_medals
FROM Medal
WHERE country_code = 'AUS';

-- Question: Names of venues where the sport "Football" is happening.
SELECT venue
FROM Venues
WHERE sports LIKE '%Football%';

-- Question: The athlete who has participated in the most events.
SELECT Athlete.name, event_counts.event_count
FROM Athlete
JOIN (
    SELECT athleteCode, COUNT(event_name) AS event_count
    FROM Athletics
    GROUP BY athleteCode
) AS event_counts ON Athlete.athleteCode = event_counts.athleteCode
WHERE event_count = (
    SELECT MAX(event_count)
    FROM (
        SELECT COUNT(event_name) AS event_count
        FROM Athletics
        GROUP BY athleteCode
    ) AS counts
);

-- Question: All information about an athlete who won the "100m Sprint" race.
SELECT Athlete.*
FROM Athlete
JOIN Athletics ON Athlete.athleteCode = Athletics.athleteCode
WHERE Athletics.event_name = '100m Sprint'
  AND Athletics.position = 1; 

-- Question: Count of medals won by Leon Marchand.
SELECT Medal.medal_type, COUNT(Medal.medal_code) AS total_medals
FROM Medal
WHERE Medal.athleteName = 'Leon Marchand'
GROUP BY Medal.medal_type;

