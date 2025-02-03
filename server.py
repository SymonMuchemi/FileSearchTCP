#!/bin/env python3
""" Server """

import socket
from utils import parse_config_file


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
                
                with conn:
                    print(f"Connected by {addr}")
                    
                    while True:
                        data: str = conn.recv(PAYLOAD_SIZE)
                        
                        if not data:
                            break
                        conn.sendall(data)
    except Exception as e:
        print(f"Error starting the server: {e}")

if __name__ == "__main__":
    start_server()
