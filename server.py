#!/usr/bin/env python3
""" Server """

import socket
import time
import ssl
import concurrent.futures
from typing import Tuple, Union
from utils import parse_config_file
from algorithms.mmap_search import mmap_search
from algorithms.radix_search import radix_search
from logger.logger import logger

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
    logger.info(f"Connection established with: {address}")
    start_time = time.time()
    
    try:
        
        # Check if server configurations are missing
        if server_configurations is None:
            logger.debug("Server configurations missing")
            return None

        # Receive the data from the client
        data: bytes = client_socket.recv(payload_size)

        # If no data is received, print a message and return
        if not data:
            logger.debug("No data received!")
            return

        logger.info(f"Data received: {data.decode('utf-8')}")

        # Get the file path from server configurations
        file_path: path_type = server_configurations.get("linuxpath")

        if not file_path:
            logger.error("linuxpath' not found in server configurations.")
            return

        # Check if the file path is a string
        if not isinstance(file_path, str):
            logger.critical("Error: 'linuxpath' must be a string.")
            return
        
        # Perform the search
        isLineFound: bool = False
        
        if server_configurations.get('REAREAD_ON_QUERY'):
            isLineFound = mmap_search(file_path, data)
        else:
            isLineFound = radix_search(file_path, data)

        # Prepare the response based on the search result
        response: bytes = EXISTS if isLineFound else NOT_EXISTS

        # Send the response to the client
        client_socket.sendall(response)
    except BrokenPipeError:
        logger.error(f"Error: Broken pipe when sending data to {address}")
    except Exception as e:
        logger.error(f"Error at handle client: {e}")
    finally:
        execution_time = time.time() - start_time
        client_socket.close()
        logger.info(f"Connection with {address} closed, Execution Time: {execution_time:.4f} seconds")


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
            logger.debug("Server configurations missing")
            return

        PAYLOAD_SIZE = server_configurations.get("PAYLOAD_SIZE")

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

        logger.info("Listening for connections...")
        
        # Wrap the socket with SSL
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='./server.crt', keyfile='./server.key')
        server_socket = context.wrap_socket(server_socket, server_side=True)

        # Use a thread pool to handle client connections
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                logger.info("Waiting for a client to connect...")
                client_socket: socket.socket
                client_address: addr_type

                # Accept a new client connection
                client_socket, client_address = server_socket.accept()
                executor.submit(handle_client, client_socket, client_address, PAYLOAD_SIZE)

    except Exception as e:
        logger.error(f"Could not start server: {e}")


if __name__ == "__main__":
    start_server_with_threading()
