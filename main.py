# запуск uvicorn main:app --reload
from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import schemas
from database import engine, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/books/", response_model=schemas.DishOut, summary="Create a Dish")
async def books(
    book: schemas.DishIn, session: AsyncSession = Depends(get_session)
) -> models.Dish:
    new_dish = models.Dish(**book.model_dump())
    async with session.begin():
        session.add(new_dish)
    await session.commit()
    return new_dish


@app.get(
    "/recipes/",
    response_model=List[schemas.DishOutBrief],
    summary="Get a list of all recipes",
    description="Returns a sorted list of recipes by views and cooking time",
)
async def dishis(session: AsyncSession = Depends(get_session)) -> List[models.Dish]:
    res = await session.execute(
        select(models.Dish).order_by(
            desc(models.Dish.views), asc(models.Dish.cook_time)
        )
    )
    return list(res.scalars().all())


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.DishOut,
    summary="Get a specific recipe",
    description="returns the recipe by id, increments the pageview counter",
)
async def dishis_for_id(
    recipe_id: int = Path(..., title="Id of the dish."),
    session: AsyncSession = Depends(get_session),
) -> models.Dish:
    res = await session.execute(select(models.Dish).where(models.Dish.id == recipe_id))
    dish = res.scalars().first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    dish.views += 1
    await session.commit()
    await session.refresh(dish)
    return dish
