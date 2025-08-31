from typing import List, Optional

from pydantic import BaseModel, Field


class Dish(BaseModel):
    name: str = Field(
        default=...,
        title="Name of the dish",
        description="The name of the dish must contain up to 100 characters.",
        max_length=100,
    )
    cook_time: int = Field(
        title="Cooking time",
        description="Cooking time per minute",
        gt=0,
    )
    views: Optional[int] = Field(
        default=0,
        title="Number of views",
        description="The number of views, by default 0",
        ge=0,
    )
    ingredients: List[str] = Field(
        default=...,
        title="List of ingredients",
        description="A list of ingredients needed to prepare the dish",
    )
    detailed_description: Optional[str] = Field(
        default=None,
        title="Detailed description",
        description="A detailed text description of the dish",
    )


class DishIn(Dish):
    "Классс для формата ввода с тем жи набором атрибутов, что и базовый"

    ...


class DishOut(Dish):

    id: int = Field(title="dish ID", description="the integer identifier of the dish")

    class Config:
        orm_mode = True


class DishOutBrief(BaseModel):

    id: int
    name: str
    views: Optional[int]
    cook_time: int

    class Config:
        orm_mode = True  # для работы с ORM объектами
