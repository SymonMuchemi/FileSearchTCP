#!/bin/env python3
""" Server """

import socket
from utils import parse_config_file

def handle_client(client_socket, address) -> None:
    print(f"Connection established with: {address}")
    
    try:
        data = client_socket.recv(1024) # TODO: use variable
        print(f'Data received: {data}')
        server_response = b'Message received'
        client_socket.sendall(server_response)
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
        
        host_and_port_tuple: tuple = (configs.get("HOST"), configs.get("PORT"))
        PAYLOAD_SIZE = configs.get('PAYLOAD_SIZE')
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(host_and_port_tuple)
            s.listen()
            
            while True:
                conn, addr = s.accept()
                
                handle_client(conn, addr)
    except Exception as e:
        print(f"Error starting the server: {e}")

if __name__ == "__main__":
    start_server()
