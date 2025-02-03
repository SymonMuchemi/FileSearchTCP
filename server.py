#!/bin/env python3
""" Server """

import socket
import concurrent.futures
from utils import parse_config_file

def handle_client(client_socket, address, payload_size = 1024) -> None:
    print(f"Connection established with: {address}")
    
    try:
        while True:
            data = client_socket.recv(payload_size)
            if not data:
                print("No data reveived!")
                break
            print(f'Data received: {data}')
            server_response = b'Message received'
            client_socket.sendall(server_response)
    except BrokenPipeError:
        print(f'Error: Broken pipe when sending data to {address}')
    except Exception as e:
        print(f"Error starting the server: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {address} closed")

def start_server() -> None:
    try:
        configs = parse_config_file("./config/config.txt")
        
        if not configs:
            print('Server configurations missing')
            return
        
        server_address: tuple = (configs.get("HOST"), configs.get("PORT"))
        PAYLOAD_SIZE = configs.get('PAYLOAD_SIZE')
        
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
        configs = parse_config_file("./config/config.txt")
        
        if not configs:
            print('Server configurations missing')
            return
        
        server_address: tuple = (configs.get("HOST"), configs.get("PORT"))
        PAYLOAD_SIZE = configs.get('PAYLOAD_SIZE')
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        server_socket.bind(server_address)
        server_socket.listen()
        
        print('Listening for connections')
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                print("Waiting for a client to connect")
                client_socket, client_address = server_socket.accept()
                executor.submit(handle_client, client_socket, client_address, PAYLOAD_SIZE)
    
    except Exception as e:
        print(f"Error starting the server: {e}")

if __name__ == "__main__":
    # start_server()
    start_server_with_threading()
