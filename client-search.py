#!/usr/bin/env python3
""" client """

import socket
import sys
from typing import Dict, Union, Optional
from utils import parse_config_file

config_type = Dict[str, Union[str, int]] | None


def start_client() -> None:
    """
    Starts the client to connect to the server and send a message.
    """
    # Parse configuration file
    configs: config_type = parse_config_file("./config/config.txt")

    if not configs:
        print("Start client: server configurations missing")
        return

    # Extract server address and payload size from configurations
    server_address = (configs.get("HOST"), configs.get("PORT"))
    payload_size: Optional[Union[int, str, None]] = configs.get("PAYLOAD_SIZE")

    if payload_size is None:
        print("Error: Payload size is missing.")
        return

    try:
        payload_size = int(payload_size)
    except (ValueError, TypeError):
        print("Error: Payload size must be an integer.")
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Connect to the server
            s.connect(server_address)

            # Send the message provided as a command-line argument
            if len(sys.argv) < 2:
                print("Usage: client.py <message>")
                return

            message: str = sys.argv[1]
            s.sendall(message.encode("utf-8"))

            # Receive the server's response
            response: bytes = s.recv(payload_size)
            print(f"Server response: {response.decode('utf-8')}")

    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"Error starting the client: {e}")


if __name__ == "__main__":
    while True:
        start_client()
