import mysql.connector
import csv
from datetime import datetime

# Function to execute SQL commands from a file
def execute_sql_file(cursor, sql_file):
    with open(sql_file, 'r') as file:
        sql_commands = file.read()
        for command in sql_commands.split(';'):
            command = command.strip()
            if command:  
                cursor.execute(command)

# Function to convert date formats
def convert_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')  # Convert to YYYY-MM-DD
    except ValueError:
        print(f"Invalid date format: {date_str}")
        return None  

def load_csv_to_db(cursor, csv_file, table_name, skip_header=True):
    try:
        with open(csv_file, 'r', encoding='ISO-8859-1') as file:
            reader = csv.reader(file)
            # Skip the header row directly if specified
            if skip_header:
                next(reader)

            for row in reader:
                if table_name == 'Country':
                    sql = f"""INSERT INTO {table_name} (country_code, country_name)
                               VALUES (%s, %s)"""
                    cursor.execute(sql, (row[0], row[1]))
                elif table_name == 'Athlete':
                    sql = f"""INSERT INTO {table_name} (athleteCode, name, gender, country_code, event_name, birthdate, coach)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], convert_date(row[5]), row[6]))
                elif table_name == 'Event':
                    sql = f"""INSERT INTO {table_name} (event_name, sport, sport_code)
                               VALUES (%s, %s, %s)"""
                    cursor.execute(sql, (row[0], row[1], row[2]))
                elif table_name == 'Medal':
                    sql = f"""INSERT INTO {table_name} (medal_type, medal_code, athleteName, gender, discipline, event_name, code, country_code)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                elif table_name == 'Venues':
                    sql = f"""INSERT INTO {table_name} (venue, sports, date_start, date_end)
                               VALUES (%s, %s, %s, %s)"""
                    cursor.execute(sql, (row[0], row[1], convert_date(row[2]), convert_date(row[3])))
                elif table_name == 'Athletics':
                    sql = f"""INSERT INTO {table_name} (event_name, stage, gender, venue, athleteCode, athleteName, country_code, position, result, result_type)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

        print(f"Data inserted into {table_name} from {csv_file}")

    except Exception as e:
        print(f"Error processing {csv_file}: {e}")


# Function to execute a given query and fetch results
def execute_query(cursor, query):
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Exception as e:
        print(f"Error executing query: {e}")

# Establish connection to the MySQL server
try:
    connection = mysql.connector.connect(
        host='localhost',
        user='dsuser',
        password='userCreateSQL'
    )
    print("Database connection successful.")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit()

# Create a cursor object
cursor = connection.cursor()

# Execute the SQL script to create the database and tables
execute_sql_file(cursor, 'databasecreation.sql')

# Execute the Procedures.sql to create the stored procedures
execute_sql_file(cursor, 'Procedures.sql')

# Connect to the newly created database
connection.database = 'OlympicsDatabase_21341382'

# Load data from CSV files
load_csv_to_db(cursor, 'country.csv', 'Country')
load_csv_to_db(cursor, 'athletes.csv', 'Athlete', skip_header=True)
load_csv_to_db(cursor, 'events.csv', 'Event')
load_csv_to_db(cursor, 'medals.csv', 'Medal')
load_csv_to_db(cursor, 'venues.csv', 'Venues')
load_csv_to_db(cursor, 'Athletics.csv', 'Athletics')

# Commit the transaction
connection.commit()

# Menu Loop
while True:
    print("\nMenu:")
    print("1. List all event names for the sport 'Athletics'.")
    print("2. Find out how many athletes are representing each country.")
    print("3. Count the number of medals each country has won.")
    print("4. List countries that have won at least 3 medals.")
    print("5. Find athletes whose age is less than 22.")
    print("6. Count the number of athletes from Australia.")
    print("7. Count how many medals were won by athletes from Australia (AUS).")
    print("8. Names of venues where the sport 'Football' is happening.")
    print("9. The athlete who has participated in the most events.")
    print("10. All information about an athlete who won the 'Men's 100m' race.")
    print("11. Count of medals won by Leon Marchand.")
    print("12. (Procedures) Add a new athlete.")
    print("13. (Procedures) Get total medal count for an athlete.")
    print("14. (Procedures) Update an athlete.")
    print("15. (Procedures) Delete an athlete.")
    print("16. Exit")

    choice = input("Select an option (1-16): ")

    if choice == '1':
        query = "SELECT event_name FROM Event WHERE sport = 'Athletics';"
        execute_query(cursor, query)
    elif choice == '2':
        country_code = input("Enter the country code (e.g., AUS, USA): ").strip()
        query = f"SELECT country_code, COUNT(*) AS athlete_count FROM Athlete WHERE country_code = '{country_code}' GROUP BY country_code;"
        execute_query(cursor, query)
    elif choice == '3':
        query = """SELECT Country.country_name, COUNT(Medal.medal_code) AS medal_count
                   FROM Medal
                   JOIN Country ON Medal.country_code = Country.country_code
                   GROUP BY Country.country_name
                   ORDER BY medal_count DESC;"""
        execute_query(cursor, query)
    elif choice == '4':
        query = """SELECT Country.country_name, COUNT(Medal.medal_code) AS medal_count
                   FROM Medal
                   JOIN Country ON Medal.country_code = Country.country_code
                   GROUP BY Country.country_name
                   HAVING medal_count >= 3;"""
        execute_query(cursor, query)
    elif choice == '5':
        query = """SELECT athleteCode, name, birthdate,
                   TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) AS age
                   FROM Athlete
                   WHERE TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) < 22;"""
        execute_query(cursor, query)
    elif choice == '6':
        query = "SELECT COUNT(*) AS total_athletes FROM Athlete WHERE country_code = 'AUS';"
        execute_query(cursor, query)
    elif choice == '7':
        query = "SELECT COUNT(*) AS total_medals FROM Medal WHERE country_code = 'AUS';"
        execute_query(cursor, query)
    elif choice == '8':
        query = "SELECT venue FROM Venues WHERE sports LIKE '%Football%';"
        execute_query(cursor, query)
    elif choice == '9':
        query = """SELECT Athlete.name, event_counts.event_count
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
                   );"""
        execute_query(cursor, query)
    elif choice == '10':
        query = """SELECT Athlete.*
                   FROM Athlete
                   JOIN Athletics ON Athlete.athleteCode = Athletics.athleteCode
                   WHERE Athletics.event_name = 'Men''s 100m'
                     AND Athletics.position = 1
                     AND Athletics.stage = 'Final';"""
        execute_query(cursor, query)
    elif choice == '11':
        query = """SELECT Medal.medal_type, COUNT(Medal.medal_code) AS total_medals
                   FROM Medal
                   WHERE Medal.athleteName = 'Leon Marchand'
                   GROUP BY Medal.medal_type;"""
        execute_query(cursor, query)
    elif choice == '12':
        
        athleteCode = int(input("Enter athlete code: "))
        name = input("Enter athlete name: ")
        gender = input("Enter athlete gender (M/F): ")
        country_code = input("Enter country code: ")
        event_name = input("Enter event name: ")
        birthdate = input("Enter birthdate (YYYY-MM-DD): ")
        coach = input("Enter coach name: ")

        cursor.callproc('AddAthlete', (athleteCode, name, gender, country_code, event_name, birthdate, coach))
        connection.commit()  
        print("Athlete added successfully.")
        
    elif choice == '13':
        
        athleteName = input("Enter athlete name: ")
        cursor.callproc('GetAthleteMedalCount', (athleteName,))

        for result in cursor.stored_results():
            total_medals = result.fetchone()[0]
            print(f"Total medals won by {athleteName}: {total_medals}")
    
    elif choice == '14':
        
        athleteCode = int(input("Enter athlete code to update: "))
        
        
        query = f"SELECT * FROM Athlete WHERE athleteCode = {athleteCode};"
        cursor.execute(query)
        athlete = cursor.fetchone()

        if athlete:
            name = input("Enter new athlete name (or leave blank to keep current): ")
            gender = input("Enter new athlete gender (or leave blank to keep current): ")
            country_code = input("Enter new country code (or leave blank to keep current): ")
            event_name = input("Enter new event name (or leave blank to keep current): ")
            birthdate = input("Enter new birthdate (YYYY-MM-DD) (or leave blank to keep current): ")
            coach = input("Enter new coach name (or leave blank to keep current): ")

            cursor.callproc('UpdateAthlete', (
                athleteCode,
                name if name else athlete[1],  # Use current name if blank
                gender if gender else athlete[2],  # Use current gender if blank
                country_code if country_code else athlete[3],  # Use current country_code if blank
                event_name if event_name else athlete[4],  # Use current event_name if blank
                convert_date(birthdate) if birthdate else athlete[5],  # Use current birthdate if blank
                coach if coach else athlete[6]  # Use current coach if blank
            ))
            connection.commit()
            print("Athlete updated successfully.")
        else:
            print(f"No athlete found with code {athleteCode}.")

    elif choice == '15':
        
        athleteCode = input("Enter athlete code to delete: ").strip()

        
        check_query = f"SELECT COUNT(*) FROM Athlete WHERE athleteCode = '{athleteCode}';"
        cursor.execute(check_query)
        exists = cursor.fetchone()[0]

        if exists > 0:
            cursor.callproc('DeleteAthlete', (athleteCode,))
            connection.commit()
            print("Athlete deleted successfully.")
        else:
            print(f"No athlete found with code: {athleteCode}")
    
        
    elif choice == '16':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")

# Close the cursor and connection
cursor.close()
connection.close()
