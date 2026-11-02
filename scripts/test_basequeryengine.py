from app.query_engines.base import BaseQueryEngine

print(BaseQueryEngine.describe_schema.__doc__)
help(BaseQueryEngine.validate_query)

from app.query_engines.base import BaseQueryEngine
from typing import Any

try:
    BaseQueryEngine()
except TypeError as e:
    print("Good, can't instantiate:", e)


class Half(BaseQueryEngine):
    def describe_schema(self): return "x"

try:
    Half()
except TypeError as e:
    print("Good, incomplete subclass rejected:", e)

class Full(BaseQueryEngine):
    
    def describe_schema(self) -> str:
        """Return a text description of the data's structure for the LLM."""
        return ""

    def generate_query(self, question:str, schema:str)->str:
        """Ask the LLM to write a query in this engine's language."""
        return ""
    
    def validate_query(self,query:str)->None:
        """Raise QueryValidationError if the query is unsafe."""
        return 

    def execute_query(self,query:str)->list[dict[str,Any]]:
            """Run the query for real and return rows as dicts."""
            return []

try:
    obj = Full()
    print(obj, type(obj).__name__)
except TypeError as e:
    print("Good, incomplete subclass rejected:", e)
