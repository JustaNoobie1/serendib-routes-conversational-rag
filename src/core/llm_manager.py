from langchain_ollama import ChatOllama

class LLMManager:
    def __init__(self, model_name="qwen3:4b-instruct-2507-q4_K_M", temperature=0):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = None
        self.initialize_llm()

    def initialize_llm(self):
        try:
            print(f"Loading the LLM through Ollama:{self.model_name}")
            self.llm = ChatOllama(
                model = self.model_name,
                temperature = self.temperature,
                keep_alive = '30m'
            )
            print("LLM initialized successfully")
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