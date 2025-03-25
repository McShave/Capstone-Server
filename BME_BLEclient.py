import asyncio
from bleak import BleakClient, BleakGATTCharacteristic

# ESP32 BLE details
ADDRESS = "3C:8A:1F:A4:65:8A"
TEMPERATURE_UUID = "d82312ea-1422-43c7-8931-408812a8f32b"
HUMIDITY_UUID = "b2106683-c2c3-47ab-a6ef-9ca7268a8b7b"

async def main():
    async with BleakClient(ADDRESS) as client:
        # Use is_connected as a property to avoid FutureWarning
        is_connected = client.is_connected
        print(f"\n[INFO] Connected to ESP32: {is_connected}\n")

        # Print available services and characteristics
        print("[INFO] Discovered BLE Services and Characteristics:")
        for service in client.services:
            print(f"  [Service] {service.uuid}: {service.description or 'Unknown'}")
            for char in service.characteristics:
                print(f"    [Characteristic] {char.uuid}:")
                print(f"      Handle: {char.handle}")
                print(f"      Properties: {', '.join(char.properties)}")
                for descriptor in char.descriptors:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    print(f"      [Descriptor] {descriptor.uuid}: Value: {bytes(value)}")

        # Define notification callback
        def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
            if characteristic.uuid == TEMPERATURE_UUID:
                print(f"[NOTIFICATION] Temperature: {data.decode('utf-8')} °C")
            elif characteristic.uuid == HUMIDITY_UUID:
                print(f"[NOTIFICATION] Humidity: {data.decode('utf-8')} %")
            else:
                print(f"[NOTIFICATION] Unknown characteristic {characteristic.uuid}: {data.decode('utf-8')}")

        # Subscribe to temperature notifications
        await client.start_notify(TEMPERATURE_UUID, notification_handler)
        print("\n[INFO] Subscribed to temperature notifications.")

        # Subscribe to humidity notifications
        await client.start_notify(HUMIDITY_UUID, notification_handler)
        print("[INFO] Subscribed to humidity notifications.")

        print("\n[INFO] Receiving data... Press Ctrl+C to stop.")
        try:
            while True:
                await asyncio.sleep(1)  # Keep the connection alive
        except KeyboardInterrupt:
            print("\n[INFO] Stopping notifications...")

        # Unsubscribe from notifications
        await client.stop_notify(TEMPERATURE_UUID)
        await client.stop_notify(HUMIDITY_UUID)
        print("[INFO] Disconnected from ESP32.")

if __name__ == "__main__":
    asyncio.run(main())