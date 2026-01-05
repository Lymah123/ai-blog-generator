from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# Create the SQLAlchemy engine
engine = create_engine(
 settings.DATABASE_URL,
 pool_pre_ping=True,
 pool_size=10,
 max_overflow=20,
 echo=settings.APP_ENVIRONMENT == "development"
 )

# Create SessionLocal
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
class Base(DeclarativeBase):
    pass

# Dependency for FastAPI routes
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
