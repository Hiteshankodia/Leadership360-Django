from pydantic import BaseModel

class StateRequestSchema(BaseModel):
    countryid : int