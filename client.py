#!/bin/env python3
""" client """

import socket
import sys
from utils import parse_config_file


def start_client() -> None:
    configs = parse_config_file("./config/config.txt")
        
    if not configs:
        print('Server configurations missing')
        return
    
    server_address = (configs.get("HOST"), configs.get("PORT"))
    PAYLOAD_SIZE = (configs.get('PAYLOAD_SIZE'))
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(server_address)
            while True:
                s.send(bytes(sys.argv[1], 'utf-8'))
                
                data = s.recv(PAYLOAD_SIZE)
                
                print(f"Server response: {data}")

    except Exception as e:
        print(f"Error starting the client: {e}")

if __name__ == '__main__':
    start_client()    
