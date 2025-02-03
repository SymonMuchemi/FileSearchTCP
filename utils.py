#!/bin/env python3
""" utilities """

def parse_config_file(file_path: str) -> dict | None:
    configurations = {}
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                
                if line.startswith('linuxpath='):
                    configurations["path"] = line.split('=', 1)[1]
                if line.startswith('HOST='):
                    configurations["host"] = line.split('=', 1)[1]
                if line.startswith('PORT='):
                    configurations["port"] = line.split('=', 1)[1]
                if line.startswith('REREAD_ON_QUERY='):
                    configurations["reread_on_query"] = line.split('=', 1)[1]
            return configurations
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while parsing the configuration file: {e}")
    
    return None
