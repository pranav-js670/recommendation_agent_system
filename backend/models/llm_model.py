from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

class LLMModel:
    def __init__(self):
        self.model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.3)

    def generate_response(self, prompt):
        return self.model.invoke(prompt).content