import logging
import re
import uuid


from sqlalchemy import (
    create_engine, MetaData
)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import insert
from sqlalchemy.sql.expression import func, select
from sqlalchemy.orm import Session 

from db import register_tables, URL

def setup_database():
    """Setup of the database, we could use a config file for this parameters 
    as an improvement 
    
    Returns:
        sqlalchemy engine
    """

    user = 'bard'
    password = 'STORY'
    database = 'story'
    DSN = f"postgresql://{user}:{password}@postgres:5432/{database}"
    engine = create_engine(DSN)
    register_tables(engine)
    return engine

logging.getLogger().setLevel(logging.INFO)
engine = setup_database()
session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
URL = Base.classes.url

def validate_url(url):
    """regex validation for urls

    
    Arguments:
        url {str} 
    
    Returns:
        bool
    """

    RE_D = re.compile(r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
    return bool(RE_D.match(url))

def _create_url(url, session=session, model=URL):
    try:
        _hash = str(uuid.uuid4())[:5]
        instance = model(**{'text': url, 'hash': _hash})
        session.add(instance)
        session.commit()
        return instance
    except Exception as e:
        logging.warning('Exception: {}'.format(e))
        session.rollback() 
        return None
    


def create_url(url, session=session, model=URL):
    instance = _create_url(url)
    while not instance:
        instance = _create_url(url)
    return instance


def get_or_create_url(url, session=session, model=URL):
    """Save url sqlalchemy and create a uuid
    
    Arguments:
        url {str} -- [description]
    
    Keyword Arguments:
        session (default: {session})
        model (default: {URL})
    
    Returns:
        SQLalchemy instance for url
    """

    instance = session.query(model).filter_by(**{'text': url}).first()
    if instance:
        return instance
    else:
        instance = create_url(url)
    return instance

def get_or_create(model, session=session, **kwargs):
    """Equivalent functionality to django's get_or-create for sqlalchemy
    source:
    https://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    
    Arguments:
        model -- sqlalchemy db model
        session -- sqlalchemy db session
    Returns:
        sqlalchemy row
    """

    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        try:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
        except Exception as e:
            logging.warning('Exception: {}'.format(e))
            session.rollback()
        return instance

def get_url(url_hash, session=session, model=URL):
    """get url sqlalchemy
    """
    instance = session.query(model).filter_by(**{'hash': url_hash}).first()
    if instance:
        return str(instance.text)
