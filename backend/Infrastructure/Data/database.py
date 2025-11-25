from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# SQL Server connection

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://salesapp:Password123@localhost\\SQLEXPRESS/SalesOrderDB?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database and create tables"""
    from Domain.Entities.models import Customer, Item, SalesOrder, OrderLineItem
    Base.metadata.create_all(bind=engine)
