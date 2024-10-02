from app.services.query_service import load_model
from app.services.firebase_services.storage_service import store_to_firebasebase

def execute_code_from_string(code_string, data_list, count):
    # Ensure generate_graph is defined in the current scope
    formatted_code = code_string.strip()

    if formatted_code != "":
    
        formatted_code += f"""\n\ndata={data_list}

image_buffer = generate_graph(data, {count})  # Use count as an integer
store_to_firebasebase(image_buffer, "graph_{count}")
"""
    print(f"\n\nCount : {count}\n")
    exec(formatted_code, globals())

def generate_data_visualization(results, model="gemini"):
    llm = load_model(model)
    llm.load_model()
    response = llm.visualize_data(results)

    return response


