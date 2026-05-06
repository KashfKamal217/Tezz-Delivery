from pydantic import BaseModel

class MessageSchema(BaseModel):
    entry: list