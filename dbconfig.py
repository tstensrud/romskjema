import sqlite3
import json
from contextlib import contextmanager
from prettytable import PrettyTable

DB_PATH = "romskjema/db/project.db"

@contextmanager
def get_cursor():
    connect = sqlite3.connect(DB_PATH)
    cursor = connect.cursor()
    try:
        yield cursor
        connect.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
        connect.close()


def create_tables():
    with get_cursor() as cursor:
        query = """
                CREATE TABLE IF NOT EXISTS Projects (
                ProjectID INTEGER PRIMARY KEY AUTOINCREMENT,
                ProjectName TEXT NOT NULL,
                Description TEXT
                )
        """
        cursor.execute(query)
        
        query = """
            CREATE TABLE IF NOT EXISTS Buildings (
            BuildingID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProjectID INTEGER,
            BuildingName TEXT NOT NULL,
            FOREIGN KEY (ProjectID) REFERENCES Projects(ProjectID)

            )
        """
        cursor.execute(query)

        query = """ 
            CREATE TABLE IF NOT EXISTS Rooms (
            RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
            BuildingID INTEGER,
            RoomType TEXT NOT NULL,
            Floor TEXT NOT NULL,
            RoomNumber TEXT NOT NULL,
            RoomName TEXT NOT NULL,
            Area REAL,
            RoomPopulation INTEGER,
            FOREIGN KEY (BuildingID) REFERENCES Buildings(BuildingID)
            )
        """
        cursor.execute(query)

        query = """
            CREATE TABLE IF NOT EXISTS VentilationProperties (
            RoomID INTEGER,
            AirPerPerson REAL,
            AirPersonSum REAL,
            AirEmission REAL,
            AirEmissionSum REAL,
            AirProcess REAL,
            AirMinimum REAL,
            AirDemand REAL,
            AirSupply REAL,
            AirExtract REAL,
            AirChosen REAL,
            VentilationPrinciple TEXT,
            HeatExchange TEXT NOT NULL,
            RoomControl TEXT NOT NULL,
            Notes TEXT,
            DbTechnical TEXT,
            DbNeighbour TEXT,
            DBCorridor TEXT,
            System TEXT,
            Comments TEXT,
            FOREIGN KEY (RoomId) REFERENCES Rooms(RoomID)
            )
        """
        cursor.execute(query)

create_tables()

# For testing purposes
def fetch_all_data(table):
    try:
        connect = sqlite3.connect(DB_PATH)
        cursor = connect.cursor()
        
        # Fetch all records
        cursor.execute(f'SELECT * FROM {table}')
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute(f'PRAGMA table_info({table})')
        columns_info = cursor.fetchall()
        column_names = [col[1] for col in columns_info]

        # Create a PrettyTable object
        table = PrettyTable()
        table.field_names = column_names

        # Add rows to the table
        for row in rows:
            table.add_row(row)

        # Print the table
        print(table)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if connect:
            connect.close()

def get_all_tables():
    with get_cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
        result = cursor.fetchall()
        return [table[0] for table in result]

def new_project(project_name: str, description: str):
    with get_cursor() as cursor:
        query = """
                INSERT INTO Projects (projectName, Description)
                VALUES (?, ?)
        """
        cursor.execute(query, (project_name, description,))

