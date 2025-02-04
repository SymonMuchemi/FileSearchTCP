#!/usr/bin/env python3
""" Server """

import socket
import concurrent.futures
from typing import Tuple, Union
from utils import parse_config_file
from algorithms.naive import naive_search
from algorithms.hash_based_search import hash_based_search

# Type alias for address (host: str, port: int)
addr_type = Tuple[str, int]
config_type = dict[str, Union[str, int]] | None
path_type = str | int | None

EXISTS: bytes = b"STRING EXISTS\n"
NOT_EXISTS: bytes = b"STRING NOT FOUND\n"

server_configurations: config_type = parse_config_file("./config/config.txt")


def handle_client(
    client_socket: socket.socket, address: addr_type, payload_size: int = 1024
) -> None:
    """
    Handles the client connection, receives data, processes it, and sends a
    response.

    Args:
        client_socket (socket.socket): The socket object for the client
                                       connection.
        address (addr_type): The address of the connected client.
        payload_size (int, optional): The size of the payload to receive.
                                       Defaults to 1024.

    Returns:
        None

    Raises:
        BrokenPipeError: If there is an error sending data to the client.
        Exception: For any other exceptions that occur during processing.
    """
    print(f"Connection established with: {address}")

    try:
        # Check if server configurations are missing
        if server_configurations is None:
            print("Server configurations missing")
            return None

        # Receive the data from the client
        data: bytes = client_socket.recv(payload_size)

        # If no data is received, print a message and return
        if not data:
            print("No data received!")
            return

        print(f"Data received: {data.decode('utf-8')}")

        # Get the file path from server configurations
        file_path: path_type = server_configurations.get("linuxpath")

        if not file_path:
            print("Error: 'linuxpath' not found in server configurations.")
            return

        # Check if the file path is a string
        if not isinstance(file_path, str):
            print("Error: 'linuxpath' must be a string.")
            return

        # Perform the search using the naive_search algorithm
        # isLineFound: bool = naive_search(file_path, data)

        # Perform the search using the hash_based_algorithm
        isLineFound: bool = hash_based_search(file_path, data)

        # Prepare the response based on the search result
        response: bytes = EXISTS if isLineFound else NOT_EXISTS

        # Send the response to the client
        client_socket.sendall(response)
    except BrokenPipeError:
        print(f"Error: Broken pipe when sending data to {address}")
    except Exception as e:
        print(f"Error at handle client: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {address} closed")


def start_server_with_threading() -> None:
    """
    Starts a TCP server using threading to handle multiple client connections
    concurrently.
    The server configuration is expected to be provided in the
    `server_configurations` dictionary.
    The server listens for incoming connections and uses a thread pool to
    handle each client connection.

    Raises:
        Exception: If there is an error starting the server.

    Notes:
        - The server configurations should include "HOST", "PORT",
        and "PAYLOAD_SIZE".
        - The function will print messages to the console to indicate
        the server status and any errors.

    Returns:
        None
    """
    try:
        if not server_configurations:
            print("Server configurations missing")
            return

        # Extract server address and payload size from configurations
        server_address = (
            server_configurations.get("HOST"),
            server_configurations.get("PORT"),
        )

        # Create a TCP socket
        server_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )

        # Bind the socket to the server address
        server_socket.bind(server_address)
        server_socket.listen()

        print("Listening for connections")

        # Use a thread pool to handle client connections
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                print("Waiting for a client to connect...")
                client_socket: socket.socket
                client_address: addr_type

                # Accept a new client connection
                client_socket, client_address = server_socket.accept()
                executor.submit(handle_client, client_socket, client_address)

    except Exception as e:
        print(f"Error starting the server: {e}")


if __name__ == "__main__":
    start_server_with_threading()
