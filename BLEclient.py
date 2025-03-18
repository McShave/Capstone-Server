import asyncio
from bleak import BleakClient, BleakGATTCharacteristic

ADDRESS = "3C:8A:1F:50:79:22"
CHARACTERISTIC_UUID = "9f8230a6-3921-427a-99de-d675cf1352aa"  # Smoke sensor characteristic

# Callback function to handle received data
def callback(sender: BleakGATTCharacteristic, data: bytearray):
    print(f"Notification from {sender}: {data.decode('utf-8').strip()}")


async def main():
    try:
        async with BleakClient(ADDRESS) as client:
            print(f"Connected to {ADDRESS}")
            services = client.services  # Use the property instead of the method
            # services = await client.get_services()
            for service in services:
                print(f"Service: {service.uuid}")
                for char in service.characteristics:
                    print(f"Characteristic: {char.uuid}")
            # Start notifications for the characteristic
            await client.start_notify(CHARACTERISTIC_UUID, callback)
            print("Started notifications...")

            # Keep the script running to listen for notifications
            while True:
                await asyncio.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())

# import asyncio
# from bleak import BleakClient, BleakGATTCharacteristic

# # Define the ESP32 BLE address and characteristic UUID
# ADDRESS = "3C:8A:1F:50:79:22"  # Update with your ESP32 BLE address
# CHARACTERISTIC_UUID = "9f8230a6-3921-427a-99de-d675cf1352aa"  # Smoke sensor characteristic


# # Callback function to handle received data
# def callback(sender: BleakGATTCharacteristic, data: bytearray):
#     smoke_level_str = data.decode("utf-8").strip()
#     try:
#         smoke_level = int(smoke_level_str)
#         print(f"Smoke Level: {smoke_level}")
#     except ValueError:
#         print(f"Invalid data received: {smoke_level_str}")


# async def main():
#     try:
#         async with BleakClient(ADDRESS) as client:
#             print(f"Connected to {ADDRESS}")

#             # Check if the device supports notifications
#             # services = client.services  # Use services property instead of get_services()
#             # replace the above line with the following:
#             services = await client.get_services()

#             print("Available Services:")
#             for service in services:
#                 print(f"Service: {service.uuid}")
#                 for char in service.characteristics:
#                     print(f"Characteristic: {char.uuid}")

#             # Start notifications if the characteristic is found
#             await client.start_notify(CHARACTERISTIC_UUID, callback)
#             print("Started notifications...")

#             # Keep the script running to listen for notifications
#             while True:
#                 await asyncio.sleep(1)  # Keep alive for notifications

#     except Exception as e:
#         print(f"Error: {e}")


# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("Disconnected from BLE device.")
