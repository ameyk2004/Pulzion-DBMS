import os
from langchain_community.utilities.sql_database import SQLDatabase

db_user = "postgres"
db_password = "Amey1234"
db_host = "localhost"
db_name = "fastapi_db"
db_port = '5432'

# Construct the connection URI
connection_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

try:
    db = SQLDatabase.from_uri(connection_uri)
    
    # Define and execute queries
    queries = {
        "Tables": f"""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """,
        
        "Views": f"""
            SELECT table_name, view_definition 
            FROM information_schema.views
            WHERE table_schema = 'public';
        """,
        
        "Procedures": f"""
            SELECT routine_name, routine_definition
            FROM information_schema.routines
            WHERE routine_schema = 'public' 
              AND routine_type = 'PROCEDURE';
        """,
        
        "Procedure Parameters": f"""
            SELECT specific_name, parameter_name, data_type, parameter_mode
            FROM information_schema.parameters
            WHERE specific_schema = 'public';
        """,
        
        "Columns": f"""
            SELECT table_name, column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_schema = 'public';
        """,
        
        "Primary Keys": f"""
            SELECT kcu.table_name, kcu.column_name
            FROM information_schema.key_column_usage kcu
            JOIN information_schema.table_constraints tc 
              ON kcu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
              AND kcu.table_schema = 'public';
        """,
        
        "Foreign Keys": f"""
            SELECT 
                kcu.table_name AS source_table,
                kcu.column_name AS source_column,
                ccu.table_name AS referenced_table,
                ccu.column_name AS referenced_column
            FROM 
                information_schema.key_column_usage kcu
            JOIN 
                information_schema.table_constraints tc 
                ON kcu.constraint_name = tc.constraint_name
            JOIN 
                information_schema.constraint_column_usage ccu 
                ON ccu.constraint_name = tc.constraint_name
            WHERE 
                tc.constraint_type = 'FOREIGN KEY'
                AND kcu.table_schema = 'public';
        """,
        
        "Indexes": f"""
            SELECT 
                schemaname,
                tablename,
                indexname,
                indexdef
            FROM 
                pg_indexes
            WHERE 
                schemaname = 'public';
        """
    }

    # Execute queries and gather data
    database_metadata = {
        "database_name": db_name,
        "number_of_tables": 0,
        "number_of_views": 0,
        "number_of_procedures": 0,
        "procedures": {},
        "tables": {},
        "views": []
    }

    # Process Table Metadata
    tables_result = db._execute(queries["Tables"])
    database_metadata["number_of_tables"] = len(tables_result)
    
    # Process Column Metadata
    columns_result = db._execute(queries["Columns"])
    primary_keys = db._execute(queries["Primary Keys"])
    foreign_keys = db._execute(queries["Foreign Keys"])
    indexes = db._execute(queries["Indexes"])
    
    # Organize column data by table
    table_columns = {}
    for column in columns_result:
        table_name = column["table_name"]
        column_name = column["column_name"]
        
        if table_name not in table_columns:
            table_columns[table_name] = {"columns": {}, "number_of_columns": 0}
        
        # Determine if column is a primary key
        is_primary = any(pk["column_name"] == column_name and pk["table_name"] == table_name for pk in primary_keys)
        
        # Determine if column is indexed
        is_indexed = any(
            column_name in idx["indexdef"] and idx["tablename"] == table_name
            for idx in indexes
        )
        
        # Determine if column is a foreign key
        referenced_tables = [
            fk["referenced_table"] for fk in foreign_keys 
            if fk["source_table"] == table_name and fk["source_column"] == column_name
        ]
        is_foreign = len(referenced_tables) > 0
        
        # Add column metadata
        table_columns[table_name]["columns"][column_name] = {
            "isPrimaryKey": is_primary,
            "isIndexed": is_indexed,
            "isForeignKey": is_foreign,
            "ReferencedTableNames": referenced_tables
        }
        table_columns[table_name]["number_of_columns"] += 1
    
    # Add organized column data to tables section
    database_metadata["tables"] = table_columns

    # Process View Metadata
    views_result = db._execute(queries["Views"])
    database_metadata["number_of_views"] = len(views_result)
    for view in views_result:
        database_metadata["views"].append({
            "view_name": view["table_name"],
            "view_definition": view["view_definition"]
        })
    
    # Process Procedure Metadata
    procedures_result = db._execute(queries["Procedures"])
    procedure_parameters_result = db._execute(queries["Procedure Parameters"])
    database_metadata["number_of_procedures"] = len(procedures_result)
    
    for procedure in procedures_result:
        routine_name = procedure["routine_name"]
        routine_definition = procedure["routine_definition"]
        
        parameters = [
            {
                "parameter_name": param["parameter_name"],
                "data_type": param["data_type"],
                "parameter_mode": param["parameter_mode"]
            }
            for param in procedure_parameters_result 
            if param["specific_name"] == routine_name
        ]
        
        database_metadata["procedures"][routine_name] = {
            "parameters": parameters,
            "routine_definition": routine_definition
        }

    # Output the final database metadata
    print(database_metadata)

except Exception as e:
    print(f"An error occurred: {e}")
