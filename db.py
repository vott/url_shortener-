from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class URL(Base):
    """URL model
    """
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False, unique=True)
    hash = Column(String(20), nullable=False, unique=True)

def register_tables(engine):
    """Create Databases with the sqlalchemy 
    engine
    
    Arguments:
        engine
    """

    Base.metadata.create_all(engine)
