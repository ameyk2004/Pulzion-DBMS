from app.services.query_service import load_model

def execute_code_from_string(code_string):
    formatted_code = code_string.strip()
    exec(formatted_code)

def generate_data_visualization(results, model="gemini"):
    llm = load_model(model)
    llm.load_model()
    response = llm.visualize_data(results)

    return response


