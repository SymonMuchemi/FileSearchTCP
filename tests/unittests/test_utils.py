import pytest
from utils import parse_config_file


def test_parse_valid_config_file(tmp_path) -> None:
    """Tests that parse_config_file correctly parses a valid configuration
    file.
    """
    config_file = tmp_path / "config.txt"
    config_file.write_text(
        "HOST=127.0.0.1\nPORT=8080\nPAYLOAD_SIZE=1024\nDEBUG=True\n"
    )

    expected_output = {
        "HOST": "127.0.0.1",
        "PORT": 8080,
        "PAYLOAD_SIZE": 1024,
        "DEBUG": "True",
    }

    assert parse_config_file(str(config_file)) == expected_output


def test_parse_config_with_none_existing_file() -> None:
    """Test handling of a file that doesn't exist"""
    assert parse_config_file('some_none_existent_file.txt') is None


if __name__ == "__main__":
    pytest.main()
