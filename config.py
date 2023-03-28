from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#parametri per SOR
min_interval = float(5) ##5 minuti
min_n_meetings = 3

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./svo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(engine)

# cache = Cache(config={'CACHE_TYPE': 'simple'})
# cache.init_app(app)















