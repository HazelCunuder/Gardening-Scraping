import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gardening_scraper.gardening_scraper.models import Base, Category, Product

load_dotenv()

def get_engine():
    db_url = (
        f"postgresql+psycopg2://"
        f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}"
        f"/{os.getenv('POSTGRES_DB')}"
    )
    return create_engine(db_url)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)

# est executé uniquement si le fichier courant est directement executé (et pas s'il est importé ailleurs)
if __name__ == "__main__":
    init_db()