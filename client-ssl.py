#!/usr/bin/env python3
""" client """

import socket
import ssl
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
        context = ssl.create_default_context()
        with socket.create_connection(server_address) as sock:
            with context.wrap_socket(socket, server_hostname=configs.get("HOST")) as ssock:
                # Connect to the server
                ssock.sendall(bytes(sys.argv[1], 'utf-8'))
                
                response = ssock.recv(payload_size)
                print(f"Server response: {response.decode('utf-8')}")

    except Exception as e:
        print(f"Error starting the client: {e}")


if __name__ == "__main__":
    start_client()
