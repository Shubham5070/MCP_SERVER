# FILE: db.py

from sqlalchemy import (
    Column, Integer, Float, String, DateTime,
    ForeignKey, create_engine
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime, timedelta
import random
import os


# ---------------- Database Setup ----------------

DB_URL = "sqlite:///./smart_meters.db"   # Safe for Render + local

engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# ---------------- Database Models ---------------

class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)

    readings = relationship("MeterReading", back_populates="meter")


class MeterReading(Base):
    __tablename__ = "meter_readings"

    id = Column(Integer, primary_key=True)
    meter_id = Column(Integer, ForeignKey("meters.id"))
    kwh = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    meter = relationship("Meter", back_populates="readings")


# ---------------- Initialization + Seeding ----------------

def init_db():
    """
    Creates tables and seeds meters + meter_readings 
    ONLY if database is empty.
    """
    Base.metadata.create_all(engine)
    db = SessionLocal()

    # Seed meters only if empty
    if db.query(Meter).count() == 0:
        print("📦 Seeding meters...")
        seed_meters = [
            Meter(id=101, name="Ravi Kumar", status="OK"),
            Meter(id=102, name="Asha Singh", status="High Usage"),
            Meter(id=103, name="Mohit Verma", status="OK"),
        ]
        db.add_all(seed_meters)
        db.commit()
    else:
        print("ℹ️ Meter table already seeded.")

    # Seed meter readings only if empty
    if db.query(MeterReading).count() == 0:
        print("📦 Seeding 30 days of meter_readings...")
        meters = db.query(Meter).all()

        for meter in meters:
            for day in range(30):
                reading = MeterReading(
                    meter_id=meter.id,
                    kwh=round(random.uniform(5, 25), 2),
                    timestamp=datetime.utcnow() - timedelta(days=day)
                )
                db.add(reading)

        db.commit()
        print("✅ Meter readings seeded.")
    else:
        print("ℹ️ Meter readings already exist.")

    db.close()
    print("✅ Database ready.")
