import asyncio
import struct
from bleak import BleakClient, BleakScanner

# BLE device address
DEVICE_NAME = 'SuperIoT'

# UUIDs for the characteristics
UUID_HUMIDITY = "2a6f"
UUID_TEMPERATURE = "2a6e"
UUID_TIMER = "183f"

async def run():

    address = ""

    devices = await BleakScanner.discover()
    for device in devices:
        if device.name == DEVICE_NAME:
           address = device.address
    if not address:
        print("Device not found")

    async with BleakClient(address) as client:
        print(f"Connected to {DEVICE_NAME}")

        # Main loop
        while True:
            try:
                time_val = await client.read_gatt_char(UUID_TIMER)
                humid_val = await client.read_gatt_char(UUID_HUMIDITY)
                tempr_val = await client.read_gatt_char(UUID_TEMPERATURE)

                # Unpacking the values based on expected formats
                ms = struct.unpack('I', time_val)[0]
                h = struct.unpack('f', humid_val)[0]
                t = struct.unpack('f', tempr_val)[0]

                # Printing the values
                print(f"ms: {ms}; h: {h:.2f}; t: {t:.2f}")

            except Exception as e:
                print(f"Error reading data: {e}")

            await asyncio.sleep(0.5)

if __name__ == "__main__":
    try:
        # Run the asyncio event loop
        asyncio.run(run())
    except KeyboardInterrupt:
        # Quit on CTRL+C
        print("\nProgram terminated by user")