import asyncio
from bleak import BleakScanner

async def scan_ble():
    devices = await BleakScanner.discover()  # Scanning BLE devices
    for device in devices:
        print(f"Device {device.address} found, RSSI={device.rssi}")

asyncio.run(scan_ble())  # Run scanning
