import asyncio
from bleak import BleakClient

# Robot's BLE service and characteristic UUIDs
SERVICE_UUID = "0000ae00-0000-1000-8000-00805f9b34fb"
WRITE_CHARACTERISTIC_UUID = "0000ae01-0000-1000-8000-00805f9b34fb"

# Command templates for various actions
COMMANDS = {
    "DANCE": bytearray([179, 2, 2, 0, 2, 170]),  # Dance command: [-77, 2, 2, 0, 2, -86]
    "MUSIC": bytearray([179, 2, 3, 0, 3, 170]),  # Music command: [-77, 2, 3, 0, 3, -86]
    "STORY": bytearray([179, 2, 1, 0, 1, 170]),  # Story command: [-77, 2, 1, 0, 1, -86]
    "EXERCISE": bytearray([179, 2, 0, 0, 0, 170]),  # Exercise command: [-77, 2, 0, 0, 0, -86]
    "VOICE": bytearray([179, 2, 4, 0, 4, 170])  # Voice adjustment command: [-77, 2, 4, 0, 4, -86]
}

def calculate_checksum(command):
    """
    Calculate checksum for the command and update the command array.
    
    :param command: The byte array representing the command.
    :return: The byte array with an updated checksum.
    """
    checksum = command[2] + command[3]  # bArr[4] = bArr[2] + bArr[3]
    command[4] = checksum & 0xFF  # Ensure it's within byte range (0-255)
    return command

async def send_command_to_robot(address, command_name):
    """
    Connects to the BLE device at the specified address and sends a command based on the command name.
    
    :param address: BLE MAC address of the robot.
    :param command_name: The command name to send (e.g., "DANCE", "MUSIC").
    """
    if command_name not in COMMANDS:
        print(f"Unknown command: {command_name}")
        return

    # Get the command byte array
    command = COMMANDS[command_name]
    # Calculate checksum and update the command
    command = calculate_checksum(command)

    async with BleakClient(address) as client:
        print(f"Connected to {address}")

        # Verify the service is available
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid}, Properties: {characteristic.properties}")

        # Add a small delay before sending the command
        await asyncio.sleep(2)

        # Write the command to the characteristic
        try:
            print(f"Sending {command_name} command to characteristic {WRITE_CHARACTERISTIC_UUID}...")
            await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, command, response=False)
            print(f"{command_name} command sent successfully!")
        except Exception as e:
            print(f"Failed to send command: {e}")

# Robot's MAC address
ROBOT_MAC_ADDRESS = "B4:5F:3A:3A:1C:AB"  # Replace with the robot's MAC address

if __name__ == "__main__":
    command = input("Enter command (DANCE, MUSIC, STORY, EXERCISE, VOICE): ").strip().upper()
    asyncio.run(send_command_to_robot(ROBOT_MAC_ADDRESS, command))
