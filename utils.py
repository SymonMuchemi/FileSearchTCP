#!/usr/bin/env python3
""" utilities """


from typing import Tuple, Union
from logger.logger import logger

addr_type = Tuple[str, int]


def parse_config_file(file_path: str) -> dict[str, Union[str, int]] | None:
    """
    Parses a configuration file and returns the configurations
    as a dictionary. The configuration file should have key-value pairs in
    the format "KEY=VALUE". Keys "PORT" and "PAYLOAD_SIZE" will have their
    values converted to integers.
    Args:
        file_path (str): The path to the configuration file.
    Returns:
        dict | None: A dictionary containing the configurations if the file
                     is successfully parsed,
                    None if the file is not found or an error occurs during
                    parsing.
    Raises:
        FileNotFoundError: If the configuration file is not found.
        Exception: If an error occurs during parsing.
    Example:
        Given a configuration file 'config.txt' with the following
        content:
            HOST=127.0.0.1
            PORT=8080
            PAYLOAD_SIZE=1024
            DEBUG=True

        The function will return:
            {
                'HOST': '127.0.0.1',
                'PORT': 8080,
                'PAYLOAD_SIZE': 1024,
                'DEBUG': 'True'
            }
    """

    configurations: dict = {}

    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()

                key: str
                val: str | int
                key, val = line.split("=", 1)

                if key in ["PORT", "PAYLOAD_SIZE"]:
                    val = int(val)

                configurations[key] = val

            return configurations
    except FileNotFoundError:
        logger.debug(f"Error: Configuration file '{file_path}' not found.")
        return None
    except Exception as e:
        logger.debug(f"Error parsing the configuration file: {e}")
        return None

    return None


server_configurations = parse_config_file("./config/config.txt")
