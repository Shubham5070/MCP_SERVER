# FILE: seed_readings.py

from smart_meter_mcp import SessionLocal, MeterReading, Meter
from datetime import datetime, timedelta
import random

db = SessionLocal()

meters = db.query(Meter).all()

print("📦 Adding dummy meter_readings...")

for meter in meters:
    for day in range(30):
        reading = MeterReading(
            meter_id=meter.id,
            kwh=round(random.uniform(5, 25), 2),
            timestamp=datetime.utcnow() - timedelta(days=day)
        )
        db.add(reading)

db.commit()
db.close()

print("✅ Successfully added 30 days of readings for all meters.")
