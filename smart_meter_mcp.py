# FILE: smart_meter_mcp.py

from fastmcp import FastMCP
import os
from sqlalchemy import func

from db import SessionLocal, Meter, MeterReading, init_db

print("🚀 Starting Smart Meter MCP Server...")

# Initialize DB (create tables + seed data)
init_db()

mcp = FastMCP("SmartMeter")


# ----------------------- Helpers -----------------------
def get_meter(meter_id: int):
    """Fetch just the meter row."""
    session = SessionLocal()
    try:
        return session.query(Meter).filter_by(id=meter_id).first()
    finally:
        session.close()


def get_total_usage(meter_id: int) -> float:
    """Compute total kWh for a meter from readings."""
    session = SessionLocal()
    try:
        total = (
            session.query(func.sum(MeterReading.kwh))
            .filter(MeterReading.meter_id == meter_id)
            .scalar()
        )
        return float(total) if total is not None else 0.0
    finally:
        session.close()


# ----------------------- Tools -------------------------
@mcp.tool()
def get_meter_info(meter_id: int) -> dict:
    """Get full meter info: name, status."""
    meter = get_meter(meter_id)
    return {
        "name": meter.name if meter else "Unknown",
        "status": meter.status if meter else "Unknown",
    }


@mcp.tool()
def get_usage(meter_id: int) -> float:
    """Get total usage by summing readings."""
    return get_total_usage(meter_id)


@mcp.tool()
def get_bill(meter_id: int) -> int:
    """Compute bill = usage * rate."""
    usage = get_total_usage(meter_id)
    rate = 7  # ₹7 per kWh
    return int(usage * rate)


@mcp.tool()
def get_status(meter_id: int) -> str:
    """If usage > threshold, return High Usage."""
    usage = get_total_usage(meter_id)
    return "High Usage" if usage > 400 else "OK"


@mcp.tool()
def get_customer_info(meter_id: int) -> str:
    """Get customer name."""
    meter = get_meter(meter_id)
    return meter.name if meter else "Unknown Customer"


# ----------------------- Server ------------------------
if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 8000))
        print(f"🌐 Starting MCP server on port {port}...")

        mcp.run(
            transport="sse",
            host="0.0.0.0",
            port=port,
        )
    except Exception as e:
        print(f"❌ Server crashed: {e}")
        import traceback
        traceback.print_exc()
