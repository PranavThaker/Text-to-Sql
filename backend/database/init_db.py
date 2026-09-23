from models import Base
from connection import get_engine

def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    
init_db()