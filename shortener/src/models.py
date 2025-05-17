from pydantic import BaseModel


class TextInput(BaseModel):
    text: str
    correlation: float = 0.5