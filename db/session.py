from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:@localhost/serial_stories_extractor?charset=utf8mb4', echo=True)
Session = sessionmaker(bind=engine, expire_on_commit=False)
