import asyncio
from bleak import BleakClient, BleakGATTCharacteristic
from db_handler import DBHandler  # Import database handler
from datetime import datetime

# ESP32 BLE details
ESP32_DEVICES = [
    {"address": "3C:8A:1F:A4:65:8A", "temperature_uuid": "d82312ea-1422-43c7-8931-408812a8f32b", "humidity_uuid": "b2106683-c2c3-47ab-a6ef-9ca7268a8b7b"},
    # Add more ESP32 devices here
]

db = DBHandler()

async def handle_device(device):
    async with BleakClient(device["address"], timeout=30.0) as client:
        is_connected = client.is_connected
        print(f"\n[INFO] Connected to ESP32: {is_connected}\n")

        # Register sensor in database
        descriptor_to_name = {}  # Map descriptors to their names
        registered_sensors = set()  # Track already registered sensor names
        for service in client.services:
            for char in service.characteristics:
                for descriptor in char.descriptors:
                    try:
                        # Use descriptor value as the sensor name
                        sensor_name = (await client.read_gatt_descriptor(descriptor.handle)).decode('utf-8').strip()
                        if sensor_name and sensor_name not in registered_sensors:  # Skip empty or duplicate names
                            sensor_id = db.add_sensor(sensor_name)
                            descriptor_to_name[char.uuid] = sensor_name  # Map UUID to descriptor name
                            registered_sensors.add(sensor_name)  # Mark as registered
                            print(f"[INFO] Registered sensor: {sensor_name} with ID: {sensor_id}")
                        elif not sensor_name:
                            print("[WARNING] Skipping empty sensor name.")
                        else:
                            print(f"[WARNING] Skipping duplicate sensor name: {sensor_name}")
                    except Exception as e:
                        print(f"[ERROR] Failed to read descriptor: {e}")

        # Define notification callback
        def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            value = data.decode('utf-8')  # Use the raw data from ESP32, including units
            sensor_name = descriptor_to_name.get(characteristic.uuid, "Unknown Sensor")
            print(f"[NOTIFICATION] {timestamp} - {sensor_name}: {value}")

        # Subscribe to notifications
        await client.start_notify(device["temperature_uuid"], notification_handler)
        await client.start_notify(device["humidity_uuid"], notification_handler)
        print("\n[INFO] Subscribed to notifications.")

        try:
            while True:
                await asyncio.sleep(1)  # Keep the connection alive
        except asyncio.CancelledError:
            print("\n[INFO] Program interrupted. Cleaning up...")
            raise
        finally:
            await client.stop_notify(device["temperature_uuid"])
            await client.stop_notify(device["humidity_uuid"])
            db.remove_sensor_data_by_device(device["address"])
            print("[INFO] Disconnected from ESP32.")

async def main():
    tasks = [handle_device(device) for device in ESP32_DEVICES]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        print("[INFO] Program interrupted. Exiting gracefully.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Program terminated by user.")