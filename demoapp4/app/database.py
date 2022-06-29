from deta import Deta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
deta = Deta(settings.DETA_SECRET)       # configure your Deta project
db = deta.Base(settings.DETA_BASE)      # access your DB


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
