#!/usr/bin/env python3
""" Server """

import socket
import concurrent.futures
from utils import server_configurations
from algorithms.naive import naive_search


def handle_client(client_socket, address, payload_size=1024) -> None:
    print(f"Connection established with: {address}")

    try:
        while True:
            data = client_socket.recv(payload_size)
            
            if not data:
                print("No data reveived!")
                break
            
            print(f"Data received: {data}")
            
            if type(data) == bytes:
                data = data.decode('utf-8')
            
            isLineFound = naive_search(
                server_configurations.get('linuxpath'),
                data.decode('utf-8')
            )
            
            if isLineFound:
                response = b"STRING FOUND"
            else:
                response = b'STRING NOT FOUND'

            client_socket.sendall(response)
    except BrokenPipeError:
        print(f"Error: Broken pipe when sending data to {address}")
    except Exception as e:
        print(f"Error starting the server: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {address} closed")


def start_server() -> None:
    try:
        if not server_configurations:
            print("Server configurations missing")
            return

        server_address: tuple = (server_configurations.get("HOST"), server_configurations.get("PORT"))
        PAYLOAD_SIZE = server_configurations.get("PAYLOAD_SIZE")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(server_address)
            s.listen()

            while True:
                conn, addr = s.accept()

                handle_client(conn, addr, PAYLOAD_SIZE)
    except Exception as e:
        print(f"Error starting the server: {e}")


def start_server_with_threading() -> None:
    try:
        if not server_configurations:
            print("Server configurations missing")
            return

        server_address: tuple = (server_configurations.get("HOST"), server_configurations.get("PORT"))
        PAYLOAD_SIZE = server_configurations.get("PAYLOAD_SIZE")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_socket.bind(server_address)
        server_socket.listen()

        print("Listening for connections")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                print("Waiting for a client to connect...")
                client_socket, client_address = server_socket.accept()
                executor.submit(
                    handle_client, client_socket, client_address, PAYLOAD_SIZE
                )

    except Exception as e:
        print(f"Error starting the server: {e}")


if __name__ == "__main__":
    # start_server()
    start_server_with_threading()
