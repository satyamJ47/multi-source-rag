import os
from abc import ABC, abstractmethod
from groq import Groq

class BaseLLMClient(ABC):
    @abstractmethod
    def generate(self, prompt:str)->str:
        pass

class GroqClient(BaseLLMClient):
    def __init__(self):
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.model = os.environ.get("GROQ_MODEL","openai/gpt-oss-20b")
        pass

    def generate(self, prompt:str)->str:
        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        print("--------Response----------")
        print(response)
        return response.choices[0].message.content

_PROVIDERS = {
    "groq": GroqClient,
}

_client = None

def get_llm_client() -> BaseLLMClient:
    global _client
    if _client is None:
        provider_name = os.environ.get("LLM_PROVIDER", "groq")
        provider_class = _PROVIDERS.get(provider_name)
        if provider_class is None:
            raise ValueError(f"Unknown LLM_PROVIDER '{provider_name}'")
        _client = provider_class()
    return _client