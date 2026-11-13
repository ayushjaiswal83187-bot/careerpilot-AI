from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Username: root, Password: (khali), Database: careerpilot_ai
DATABASE_URL = "mysql+pymysql://root:ayush45@localhost:3306/careerpilot_ai"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()