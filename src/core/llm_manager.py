from langchain_openai import ChatOpenAI
import os

class LLMManager:
    def __init__(self, model_name=None, temperature=0):
        self.provider = os.getenv('LLM_PROVIDER', 'ollama').lower().strip()
        self.model_name = os.getenv('GROQ_MODEL', "openai/gpt-oss-120b")
        self.temperature = temperature
        self.llm = None

        self.initialize_llm()

    def initialize_llm(self):
        try:
            print(f"Loading the hosted LLM through Groq:{self.model_name}")
            self.llm = ChatOpenAI(
                model = self.model_name,
                temperature = self.temperature,
                api_key= os.environ['GROQ_API_KEY'],
                base_url= 'https://api.groq.com/openai/v1',
                max_completion_tokens=2048,
                use_responses_api=False
            )
            print("Groq LLM initialized successfully")
        except Exception as e:
            print(f"Error initializing the LLM: {e}")
            raise

    def generate(self, message):
        if self.llm is None:
            raise ValueError(
                "LLM has not been initialized."
            )
        response = self.llm.invoke(message)
        return response

    def get_llm(self):
        return self.llm