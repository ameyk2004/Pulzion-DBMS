class PromptProvider:
        
    def generateDescriptionPromptText(self,context_string):
        return f"""
        I have provided a JSON structure containing metadata about a database, including tables, views, and procedures. 
        Please analyze the data step by step and return a new JSON structure with the following requirements:

        1. Database Description:
        - Provide a brief description of the overall database, including its purpose and primary functions.

        2. Table Descriptions:
        For each table, generate:
        - A description summarizing the table's purpose.
        - For each column in the table, provide:
            - A description of its role and significance.
        - Analyze relationships with other tables:
            - Provide descriptions of these relationships, including the cardinality (e.g., one-to-many, many-to-one).

        3. View Descriptions:
        For each view, provide:
        - A description of what the view represents.
        - Explain how it relates to the underlying tables and any relevant filters or calculations.

        4. Output Structure:
        - Organize the resulting descriptions clearly within a new JSON format, maintaining clarity and conciseness for each description.

        Processing Steps:
        Please follow these processing steps while analyzing the JSON data:

        1. Overall Database Analysis:
        - Begin with a high-level overview of the database.

        2. Independent Tables:
        - Identify and analyze all independent tables first.
        - For each independent table, repeat the description process as outlined.

        3. Dependent Tables:
        - Identify dependent tables that relate to the independent ones.
        - Repeat the description process for each dependent table accordingly.

        4. Views Analysis:
        - For each view, generate a description based on its definition and context within the database.

        5. Final Output:
        - Ensure the final output is in a well-structured JSON format with clear and concise descriptions.
        - IMPORTANT NOTE: For final output maintain the original metadata and combine it with descriptions
        - IMPORTANT NOTE: Return only the JSON structure and avoid any extra commentary, key points, or explanations

        Here is the JSON data:
        {context_string}
    """

    def generateQueryPromptText(self,query, context_string):

        return f"""
        I am providing you with a JSON structure containing metadata about a database, including tables, columns, relationships, and views. Based on this information, please analyze the following user query and generate the corresponding SQL queries.
        - IMPORTANT NOTE: FOR ANY QUERY Do not USE ANY DBMS SPECIFIC COMMAND INSTEAD USE NESTED SELECT QUERIES IF REQUIRED
        User Query: "{query}"

        Context JSON:
        {context_string}

        It is possible that multiple SQL queries are needed to answer this user query (e.g., queries involving joins, aggregations, or filtering across different tables). 
        Please generate all necessary SQL queries and return them in a structured JSON format as follows:
        {{
            "queries": [
                {{ "output": " --query1 " }},
                {{ "output": " --query2 " }},
                ...
            ]
        }}
        - IMPORTANT NOTE: Return only the JSON structure and avoid any extra commentary, key points, or explanations
        """
    
    def generateOptimizedQueryPromptText(self,query,context_string):
        prompt = f"""

        Here is the generated SQL query based on the users request:

        -- Original Query
        {query}

        Please optimize this query for better performance, ensuring that the required results remain unchanged.
        - IMPORTANT NOTE: FOR ANY QUERY Do not USE ANY DBMS SPECIFIC COMMAND INSTEAD USE NESTED SELECT QUERIES IF REQUIRED

        I am providing a json structure containing metadata about a database, including tables, columns, relationships, and views which also conatins columns which are indexed
        Use this information to optimize the query.
        {context_string}
        
        Important Instructions:
        Please optimize this query for better performance, ensuring that the required results remain unchanged.
        It is possible that the query doesn't need any optimization. In that case, return the original query
        Return the optimized query in the following JSON format:

        {{
            "queries": [
                {{ "optimized_output": " --optimized_query or original sql query if optimization not required " }},
                {{ "optimized_output": " --optimized_query or original sql query if optimization not required " }},
                ...
            ]
        }}

        """
        return prompt
    

    def generateVisualizationPromptText(self, results):
        return f"""
    I have retrieved multiple datasets from my SQL database, which are presented below. Each dataset corresponds to a different query. Your task is to analyze each dataset and determine the best way to present the information. Specifically:

    1. For each dataset, identify key patterns, trends, or relationships within the data (e.g., correlations, comparisons, distributions).
    2. Based on the analysis of each dataset, recommend whether the data is best represented as a graphical visualization (such as a bar chart, pie chart, line chart, scatter plot, etc.) or a tabular format.
    3. If a graph is suitable, specify the type of chart and explain why it is ideal for the data's structure and insights (e.g., comparing categories, displaying trends, or highlighting proportions).
    4. If a graph is not appropriate, recommend an alternative format (such as a table) and explain why it better conveys the data.
    5. Consider factors like data types (categorical, numerical, etc.), value ranges, and whether the dataset lends itself to comparisons, distributions, or temporal trends.

    Datasets from SQL query:
    {results}

    Each dataset in the results array should be processed independently, and appropriate representations should be determined for each.

    STRICTLY FOLLOW RESPONSE FORMAT

    ALSO GENERATE PYTHON CODE TO CREATE THE GRAPHICAL VISUALIZATION OR THE TABLE FORMAT USING MATPLOTLIB.

    only Python code no other code also kindly return correct json format adhering to given response example.

    Response format:
    {{
        "response": [
            {{
                "Is graph possible": "true or false",
                "graph type": " -- or 'table' if graph generation not needed",
                "Insights": "This should be a list of insights about the observations of results given",
                "Code": "Return Python code for matplotlib-based visualization or table ",
            }},
            {{
                ...
            }}
        ]
    }}
    """
