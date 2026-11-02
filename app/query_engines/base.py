from abc import ABC, abstractmethod
from typing import Any

from app.models.schemas import QueryResult

MAX_ROWS = 50 # cap before rows reach the LLM
CANNOT_ANSWER = "CANNOT_ANSWER"  # sentinel the LLM returns when the data can't answer

class QueryValidationError(Exception):
    """Raised when a generated query is unsafe or malformed"""

class BaseQueryEngine(ABC):
    @abstractmethod
    def describe_schema(self) -> str:
        """Return a text description of the data's structure for the LLM."""

    @abstractmethod
    def generate_query(self, question:str, schema:str)->str:
        """Ask the LLM to write a query in this engine's language."""

    @abstractmethod
    def validate_query(self,query:str)->None:
        """Raise QueryValidationError if the query is unsafe."""

    @abstractmethod
    def execute_query(self,query:str)->list[dict[str,Any]]:
         """Run the query for real and return rows as dicts."""

    def run(self, question: str)->QueryResult:
        schema = self.describe_schema()
        query = self.generate_query(question,schema)
        if query.strip() == CANNOT_ANSWER:
            return QueryResult(
                query="", rows=[],
                answer="I can't answer that from the available data.",
            )
        self.validate_query(query)
        rows = self.execute_query(query)
        answer = self._format_answer(question, query, rows)
        return QueryResult(query=query, rows=rows, answer=answer)

    def _format_answer(self,question: str, query: str, rows: list[dict])-> str:
        raise NotImplementedError  # we'll build this in step 4