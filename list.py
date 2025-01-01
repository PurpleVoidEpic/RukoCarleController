import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_IDENTIFIER = "b4:5f:3a:3a:1c:ab"  # Replace with your device's MAC address

async def get_characteristic_uuids():
    print("Scanning for devices...")
    devices = await BleakScanner.discover()

    target_device = None
    for device in devices:
        print(f"Found device: {device.name} - {device.address}")
        if device.address.lower() == DEVICE_IDENTIFIER:
            target_device = device
            break

    if not target_device:
        print("Device not found!")
        return

    print(f"Found target device: {target_device.name} ({target_device.address})")

    async with BleakClient(target_device.address) as client:
        print(f"Connected to {target_device.name}")
        print("Discovering services...")

        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid}")
                print(f"    Properties: {characteristic.properties}")

    print("Disconnected from the device.")


if __name__ == "__main__":
    asyncio.run(get_characteristic_uuids())
