from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Word(Base):
    """Words model
    """

    __tablename__ = 'word'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False, unique=True)
    titles = relationship("Title")

class URL(Base):
    """URL model
    """
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False, unique=True)
    hash = Column(String(20), nullable=False, unique=True)

class Title(Base):
    """Title Model
    """

    __tablename__ = 'title'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    parent_id = Column(Integer, ForeignKey('word.id'))
    words = relationship("Word", back_populates="titles")

def register_tables(engine):
    """Create Databases with the sqlalchemy 
    engine
    
    Arguments:
        engine
    """

    Base.metadata.create_all(engine)
