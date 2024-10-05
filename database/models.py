from sqlalchemy.orm import declarative_base, DeclarativeBase, relationship
from sqlalchemy import MetaData, String, Column, Integer, ForeignKey

Base: DeclarativeBase = declarative_base()


class Breed(Base):
    __tablename__ = 'breed'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    kitten = relationship('Kitten', back_populates='breed')


class Kitten(Base):
    __tablename__ = 'kitten'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    breed_id = Column(Integer, ForeignKey('breed.id', ondelete='CASCADE'), nullable=False)
    age_month = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    color = Column(String, nullable=False)

    breed = relationship('Breed', back_populates='kitten')