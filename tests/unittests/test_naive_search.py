#!/usr/bin/env python3
""" Test cases for the naive_search module """


import pytest
from algorithms.naive import read_file_generator


def test_read_file_generator(tmp_path) -> None:
    """Test the read file generator function on a non-empty file """
    test_file = tmp_path / "test_file.txt"
    test_content = "  line 1  \nline 2\n  line 3  \n"
    test_file.write_text(test_content)
    
    expected_output_list = ["line 1", "line 2", "line 3"]
    
    result_lines = list(read_file_generator(str(test_file)))
    
    assert result_lines == expected_output_list
    

if __name__ == "__main__":
    pytest.main()
    
