from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_PATH = "postgresql://postgres:Ka1NEo05x@localhost/q2g"

engine = create_engine(SQL_DATABASE_PATH)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()