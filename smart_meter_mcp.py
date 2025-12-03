# FILE: smart_meter_mcp.py

from fastmcp import FastMCP
import os
from db import SessionLocal, Meter, init_db

print("🚀 Starting Smart Meter MCP Server...")

# Initialize DB (create tables + seed data)
init_db()

# Create MCP server instance
mcp = FastMCP("SmartMeter")


# ----------------------- Helper -----------------------
def fetch_meter(meter_id: int):
    """
    Retrieve a Meter record from the database.
    """
    session = SessionLocal()
    meter = session.query(Meter).filter_by(id=meter_id).first()
    session.close()
    return meter


# ----------------------- Tools ------------------------
@mcp.tool()
def get_meter_info(meter_id: int) -> dict:
    """Get full meter info: name, status."""
    m = fetch_meter(meter_id)
    return {
        "name": m.name if m else "Unknown",
        "status": m.status if m else "Unknown",
    }


@mcp.tool()
def get_usage(meter_id: int) -> float:
    """Get total usage by summing last 30 readings."""
    m = fetch_meter(meter_id)
    if not m:
        return 0.0
    return sum(r.kwh for r in m.readings)


@mcp.tool()
def get_bill(meter_id: int) -> int:
    """Compute bill based on usage * fixed rate."""
    m = fetch_meter(meter_id)
    if not m:
        return 0
    usage = sum(r.kwh for r in m.readings)
    rate = 7  # ₹7 per kWh
    return int(usage * rate)


@mcp.tool()
def get_status(meter_id: int) -> str:
    """If usage > threshold, return High Usage."""
    m = fetch_meter(meter_id)
    if not m:
        return "Unknown"

    usage = sum(r.kwh for r in m.readings)
    return "High Usage" if usage > 400 else "OK"


@mcp.tool()
def get_customer_info(meter_id: int) -> str:
    """Get customer name."""
    m = fetch_meter(meter_id)
    return m.name if m else "Unknown Customer"


# ----------------------- Server -----------------------
if __name__ == "__main__":
    """
    Entry point of the MCP server.
    Starts the FastMCP SSE server.
    """
    try:
        port = int(os.getenv("PORT", 8000))
        print(f"🌐 Starting MCP server on port {port}...")

        mcp.run(
            transport="sse",
            host="0.0.0.0",
            port=port
        )

    except Exception as e:
        print(f"❌ Server crashed: {e}")
        import traceback
        traceback.print_exc()
