import asyncio
from bleak import BleakClient
import keyboard

# Robot's BLE service and characteristic UUIDs
SERVICE_UUID = "0000ae00-0000-1000-8000-00805f9b34fb"
WRITE_CHARACTERISTIC_UUID = "0000ae01-0000-1000-8000-00805f9b34fb"

# Command templates for various actions
COMMANDS = {
"REMOVED IN script check the other one version only movment is here"
}

MOVEMENT_COMMANDS = {
    "W": bytearray([182, 6, 0, 5, 3, 0, 0, 0, 0, 170]),  # Move forward
    "A": bytearray([182, 6, 0, 5, 5, 0, 0, 0, 0, 170]),  # Turn left
    "S": bytearray([182, 6, 0, 5, 7, 0, 0, 0, 0, 170]),  # Move backward
    "D": bytearray([182, 6, 0, 5, 1, 0, 0, 0, 0, 170])   # Turn right
}

def calculate_checksum(command):
    checksum = sum(command[2:8])  # Sum relevant bytes for checksum
    command[8] = checksum & 0xFF  # Ensure checksum is within byte range (0-255)
    return command

async def send_command(client, command):
    """
    Sends a command to the robot using the specified BLE client.
    """
    command = calculate_checksum(command)
    try:
        await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, command, response=False)
        print(f"Command sent: {command}")
    except Exception as e:
        print(f"Failed to send command: {e}")

async def control_bot(address):
    async with BleakClient(address) as client:
        print(f"Connected to {address}")
        print("Use W, A, S, D keys to control the robot. Press Q to quit.")

        while True:
            if keyboard.is_pressed("q"):
                print("Exiting control mode.")
                break
            for key, command in MOVEMENT_COMMANDS.items():
                if keyboard.is_pressed(key):
                    print(f"Key pressed: {key}")
                    print(f"Command before checksum: {command}")
                    command = calculate_checksum(command)
                    print(f"Command after checksum: {command}")
                    await send_command(client, command)
                    await asyncio.sleep(0.1)  # Prevent spamming commands

async def send_command_to_robot(address, command_name):
    """
    Connects to the BLE device and sends a specific command.
    """
    if command_name not in COMMANDS:
        print(f"Unknown command: {command_name}")
        return

    command = calculate_checksum(COMMANDS[command_name])

    async with BleakClient(address) as client:
        print(f"Connected to {address}")
        try:
            print(f"Sending {command_name} command...")
            await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, command, response=False)
            print(f"{command_name} command sent successfully!")
        except Exception as e:
            print(f"Failed to send command: {e}")

# Robot's MAC address
ROBOT_MAC_ADDRESS = "B4:5F:3A:3A:1C:AB"  # Replace with the robot's MAC address

if __name__ == "__main__":
    print("Options: CONTROL")
    mode = input("Enter mode: ").strip().upper()

    if mode == "CONTROL":
        asyncio.run(control_bot(ROBOT_MAC_ADDRESS))
    else:
        asyncio.run(send_command_to_robot(ROBOT_MAC_ADDRESS, mode))
