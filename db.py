from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Username: root, Password: (khali), Database: careerpilot_ai
DATABASE_URL = "mysql+pymysql://careerpilotAI_missingwet:8c17a9707e834fe1163bed6f6d3b42b87d692a91@a8e7ac.h.filess.io:3306/careerpilotAI_missingwet"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
