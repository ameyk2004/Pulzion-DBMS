from app.models.llm import LLM
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from app.models.data.prompts import PromptProvider
load_dotenv()

class GeminiLLM(LLM):

    def __generateDescriptionPrompt(self,context_json):
        context_string = json.dumps(context_json, indent=2)
        prompt = self.promptProvider.generateDescriptionPromptText(context_string)
        return prompt

    def __generateQueryPrompt(self,query, context_json):
        context_string = json.dumps(context_json, indent=2)
        prompt = self.promptProvider.generateQueryPromptText(query, context_string)
        return prompt
    
    def __generateOptimizedQueryPrompt(self,query, context_json):
        context_string = json.dumps(context_json, indent=2)
        prompt = self.promptProvider.generateOptimizedQueryPromptText(query, context_string)
        return prompt
    
    def __appendToHistory(self,role:str, res:str):
        self.history.append({"role": role, "content": res})

    def __send_message_to_model(self,prompt):
        response = self.chat_session.send_message(prompt)
        if self.preserve_history:
            self.__appendToHistory("user", prompt)
            self.__appendToHistory("assistant", json.dumps(response.text, indent=0))
        return response.text

    def __init__(self, preserve_history:bool):
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        self.GEMINI_MODEL_NAME = os.getenv('GEMINI_MODEL_NAME')
        genai.configure(api_key=self.GEMINI_API_KEY)
        
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        
        if(preserve_history):
            self.preserve_history = True
        else:
            self.preserve_history = False
        self.history = []

        self.promptProvider = PromptProvider()

    def load_model(self):
        self.model = genai.GenerativeModel(
            model_name=self.GEMINI_MODEL_NAME,
            generation_config=self.generation_config,
        )
        self.chat_session = self.model.start_chat(
            history=self.history
        )
    
    def set_context(self, context):
        # Generate a descriptive json context first
        response_text = self.__send_message_to_model(self.__generateDescriptionPrompt(context))
        return response_text

    def generate_query(self, prompt: str, context_json) -> dict:
        response_text = self.__send_message_to_model(self.__generateQueryPrompt(prompt, context_json))
        return response_text

    def optimize_query(self, query: str, context_json) -> dict:
        response_text = self.__send_message_to_model(self.__generateOptimizedQueryPrompt(query, context_json))
        return response_text

    def run_query(self, prompt, context):
        descriptive_json_context = self.set_context(context=context)
        query = self.generate_query(prompt, descriptive_json_context)
        optimized_query = self.optimize_query(query, descriptive_json_context).replace("```json"," ").replace("```"," ")
        data = json.loads(optimized_query)
        result_queries = [query['optimized_output'].replace("\n", " ") for query in data['queries']]
        # result_query = data["optimized_output"].replace("\\n", " ")
        return result_queries

# json_context = '''{"database_name":"fastapi_db","number_of_tables":4,"number_of_views":1,"number_of_procedures":0,"procedures":{},"tables":{"users":{"columns":{"id":{"isPrimaryKey":true,"isIndexed":true,"isForeignKey":false,"ReferencedTableNames":[]},"password":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]},"email":{"isPrimaryKey":false,"isIndexed":true,"isForeignKey":false,"ReferencedTableNames":[]},"cretated_at":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]},"name":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]}},"number_of_columns":5},"posts":{"columns":{"created_at":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]},"title":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]},"published":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]},"id":{"isPrimaryKey":true,"isIndexed":true,"isForeignKey":false,"ReferencedTableNames":[]},"content":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]},"owner_id":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":true,"ReferencedTableNames":["users"]}},"number_of_columns":6},"viewpostvotes":{"columns":{"title":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]},"vote_count":{"isPrimaryKey":false,"isIndexed":false,"isForeignKey":false,"ReferencedTableNames":[]}},"number_of_columns":2},"votes":{"columns":{"post_id":{"isPrimaryKey":true,"isIndexed":true,"isForeignKey":true,"ReferencedTableNames":["posts"]},"user_id":{"isPrimaryKey":true,"isIndexed":true,"isForeignKey":true,"ReferencedTableNames":["users"]}},"number_of_columns":2}},"views":[{"view_name":"viewpostvotes","view_definition":" SELECT posts.title,\n    count(votes.post_id) AS vote_count\n   FROM (posts\n     LEFT JOIN votes ON ((posts.id = votes.post_id)))\n  GROUP BY posts.title;"}]}'''

# prompt = "Get all posts from user Amey"

# llm = GeminiLLM(preserve_history=True)
# llm.load_model()
# print(prompt)
# query = llm.run_query(prompt=prompt, context=json_context)
# print(query)
