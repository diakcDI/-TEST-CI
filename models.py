from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import JSON
from sqlalchemy.orm import mapped_column

from database import Base


class Dish(Base):
    __tablename__ = "dishes"  # имя таблицы в БД

    id = Column(Integer, primary_key=True, autoincrement=True)  # первичный ключ
    name = Column(String, nullable=False)  # название блюда
    views = mapped_column(Integer, default=0)  # количество просмотров
    cook_time = Column(Integer, nullable=False)  # время приготовления в минутах
    ingredients = Column(MutableList.as_mutable(JSON), nullable=False, default=[])
    detailed_description = Column(String, nullable=False)
