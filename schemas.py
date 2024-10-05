from pydantic import BaseModel


class BreedBase(BaseModel):
    name: str


class BreedCreate(BreedBase):
    pass


class Breed(BreedBase):
    id: int
    class Config:
        from_attributes = True


class KittenBase(BaseModel):
    name: str
    breed_id: int
    age_month: int
    description: str
    color: str


class KittenCreate(KittenBase):
    pass


class Kitten(KittenBase):
    id: int
    class Config:
        from_attributes = True