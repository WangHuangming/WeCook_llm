from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str
    category: str
    weightInGrams: int
    purchaseDate: str