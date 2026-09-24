from pydantic import BaseModel

class SQLResponse(BaseModel):
    sql:str
    explanation:str
    confidence:float