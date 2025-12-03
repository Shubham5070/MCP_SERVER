# FILE: server/db.py
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = "sqlite:///./smart_meters.db"

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class SmartMeter(Base):
    __tablename__ = "smart_meters"
    
    meter_id = Column(Integer, primary_key=True)
    name = Column(String)
    usage = Column(Float)
    bill = Column(Integer)
    status = Column(String)

def init_db():
    Base.metadata.create_all(engine)
    session = SessionLocal()

    # Seed initial data only if table is empty
    if session.query(SmartMeter).count() == 0:
        seed_data = [
            SmartMeter(meter_id=101, name="Ravi Kumar", usage=12.5, bill=420, status="OK"),
            SmartMeter(meter_id=102, name="Asha Singh", usage=20.1, bill=670, status="High Usage"),
            SmartMeter(meter_id=103, name="Mohit Verma", usage=8.2, bill=290, status="OK"),
        ]
        session.add_all(seed_data)
        session.commit()

    session.close()
