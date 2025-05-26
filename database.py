from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual database credentials
DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/demt1"

# Create the engine
engine = create_engine(
    DATABASE_URL,
    echo=False,         # Log SQL queries — set to False in production
    pool_pre_ping=True # Helps with stale connections
)

# SessionLocal class to instantiate DB sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
