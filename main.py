from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select

from database.engine import get_async_session, engine
import schemas
from database.models import Breed, Base, Kitten


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/breeds', response_model=List[schemas.Breed], responses={200: {"model": List[schemas.Breed]},
                                                                   404: {"description": "No breeds found"}})
async def get_breeds(session=Depends(get_async_session)):
    query = select(Breed)
    breeds = await session.execute(query)
    return breeds.scalars().all()


@app.post('/breeds', response_model=schemas.Breed)
async def create_breed(breed: schemas.BreedCreate, session=Depends(get_async_session)):
    new_breed = Breed(**breed.dict())
    session.add(new_breed)
    await session.commit()
    await session.refresh(new_breed)
    return new_breed


@app.get('/kittens', response_model=List[schemas.Kitten])
async def get_kittens(session=Depends(get_async_session)):
    query = select(Kitten)
    kittens = await session.execute(query)
    return kittens.scalars().all()


@app.get('/kittens/{breed_id}', response_model=List[schemas.Kitten],
         responses={404: {"description": "No kittens found"}})
async def get_kittens_by_breed(breed_id: int, session=Depends(get_async_session)):
    query = select(Kitten).where(Kitten.breed_id == breed_id)
    kittens = await session.execute(query)
    kittens = kittens.scalars().all()
    if not kittens:
        raise HTTPException(status_code=404, detail="No kittens found")
    return kittens


@app.get('/kittens/{kitten_id}', response_model=schemas.Kitten,
         responses={404: {"description": "Kitten not found"}})
async def get_kitten(kitten_id: int, session=Depends(get_async_session)):
    query = select(Kitten).where(Kitten.id == kitten_id)
    kitten = await session.execute(query)
    kitten = kitten.scalar_one_or_none()
    if not kitten:
        raise HTTPException(status_code=404, detail="Kitten not found")
    return kitten

@app.post('/kittens', response_model=schemas.Kitten)
async def create_kitten(kitten: schemas.KittenCreate, session=Depends(get_async_session)):
    new_kitten = Kitten(**kitten.dict())
    session.add(new_kitten)
    await session.commit()
    await session.refresh(new_kitten)
    return new_kitten


@app.put('/kittens/{kitten_id}', response_model=schemas.Kitten,
         responses={404: {"description": "Kitten not found"}})
async def update_kitten(kitten_id: int, kitten: schemas.KittenCreate, session=Depends(get_async_session)):
    query = select(Kitten).where(Kitten.id == kitten_id)
    kitten_db = await session.execute(query)
    kitten_db = kitten_db.scalar_one_or_none()
    if not kitten_db:
        raise HTTPException(status_code=404, detail="Kitten not found")
    for key, value in kitten.dict().items():
        setattr(kitten_db, key, value)
    await session.commit()
    await session.refresh(kitten_db)
    return kitten_db


@app.delete('/kittens/{kitten_id}', response_model=schemas.Kitten, responses={404: {"description": "Kitten not found"}})
async def delete_kitten(kitten_id: int, session=Depends(get_async_session)):
    query = select(Kitten).where(Kitten.id == kitten_id)
    kitten_db = await session.execute(query)
    kitten_db = kitten_db.scalar_one_or_none()
    if not kitten_db:
        raise HTTPException(status_code=404, detail="Kitten not found")
    session.delete(kitten_db)
    await session.commit()
    return kitten_db




