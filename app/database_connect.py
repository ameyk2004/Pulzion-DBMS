from langchain_community.utilities.sql_database import SQLDatabase

user = "postgres"
password = "Amey1234"
host = "localhost"

connection_uri = f"postgresql://{user}:{password}@{host}:5432/hotel_db"
db = SQLDatabase.from_uri(connection_uri)

db._execute("""
INSERT INTO room_types (room_type_name, description)
VALUES
    ('Single', 'Single room with a single bed'),
    ('Double', 'Double room with a double bed'),
    ('Suite', 'Luxury suite with multiple amenities'),
    ('Deluxe', 'Deluxe room with premium features');
""")