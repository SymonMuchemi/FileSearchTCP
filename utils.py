#!/bin/env python3
""" utilities """

def parse_config_file(file_path: str) -> dict | None:
    configurations = {}
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                
                key, val = line.split('=', 1)
                
                if key in ['PORT', 'PAYLOAD_SIZE']:
                    val = int(val)
                
                configurations[key] = val
            
            print(f'Server configuration dictionary: {configurations}')
            return configurations
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while parsing the configuration file: {e}")
    
    return None
