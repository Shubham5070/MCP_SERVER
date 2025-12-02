# FILE: server/smart_meter_mcp.py

from fastmcp import FastMCP
import os 

print("🚀 Starting Smart Meter MCP Server...")

mcp = FastMCP("SmartMeter")

# Hardcoded smart meter data
smart_meters = {
    101: {"name": "Ravi Kumar", "usage": 12.5, "bill": 420, "status": "OK"},
    102: {"name": "Asha Singh", "usage": 20.1, "bill": 670, "status": "High Usage"},
    103: {"name": "Mohit Verma", "usage": 8.2, "bill": 290, "status": "OK"},
}

@mcp.tool()
def get_meter_info(meter_id: int) -> dict:
    """Get complete meter information including name, usage, bill, and status"""
    print(f"📊 Tool called: get_meter_info(meter_id={meter_id})")
    return smart_meters.get(meter_id, {
        "name": "Unknown",
        "usage": None,
        "bill": None,
        "status": "Unknown"
    })

@mcp.tool()
def get_usage(meter_id: int) -> float:
    """Get electricity usage in kWh for a specific meter"""
    print(f"⚡ Tool called: get_usage(meter_id={meter_id})")
    return smart_meters.get(meter_id, {}).get("usage", 0.0)

@mcp.tool()
def get_bill(meter_id: int) -> int:
    """Get bill amount in rupees for a specific meter"""
    print(f"💰 Tool called: get_bill(meter_id={meter_id})")
    return smart_meters.get(meter_id, {}).get("bill", 0)

@mcp.tool()
def get_status(meter_id: int) -> str:
    """Get status of a specific meter (OK, High Usage, etc.)"""
    print(f"📈 Tool called: get_status(meter_id={meter_id})")
    return smart_meters.get(meter_id, {}).get("status", "Unknown")

@mcp.tool()
def get_customer_info(meter_id: int) -> str:
    """Get customer name for a specific meter"""
    print(f"👤 Tool called: get_customer_info(meter_id={meter_id})")
    return smart_meters.get(meter_id, {}).get("name", "Unknown Customer")

# Start server
if __name__ == "__main__":
    try:
        port = int(os.getenv("PORT", 8000))
        mcp.run(
            transport="sse",
            host="0.0.0.0",
            port=port
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        import traceback
        traceback.print_exc()