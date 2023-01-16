from pydantic import BaseModel

class CreateItemRequest(BaseModel):
    name: str
    description: str
    price: int