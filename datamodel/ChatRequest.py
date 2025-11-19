from pydantic import BaseModel

from datamodel.Ingredient import Ingredient
from datamodel.Message import Message


class ChatRequest(BaseModel):
    messages: list[Message]
    ingredients: list[Ingredient]