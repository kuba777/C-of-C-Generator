from project import check_all_entries
from project import check_pn
from project import combine
from project import open_file
from project import generate_pdf
from project import check_answer
from project import split_string
import os
import pytest
from unittest.mock import patch
from fpdf import FPDF



def test_check_answer():
    assert check_answer ("no") == False
    assert check_answer ("yes") == True
    assert check_answer ("not related") == False
    assert check_answer ("YES") == True
    assert check_answer ("Y") == True
    assert check_answer ("Y") == True


def test_split_string():
    assert split_string ("Test Python", 3) == ['', 'Test', 'Python']
    assert split_string ("Test Python", 5) == ['Test', 'Python']


def test_open_file():
     # Test case when the file exists
    csv_data = """Name,Age,Gender
Alice,30,Female
Bob,25,Male"""

    with open("test_data.csv", "w") as file:
        file.write(csv_data)

    result = open_file("test_data.csv")

    assert len(result) == 2
    assert result[0]["Name"] == "Alice"
    assert result[0]["Age"] == "30"
    assert result[0]["Gender"] == "Female"
    assert result[1]["Name"] == "Bob"
    assert result[1]["Age"] == "25"
    assert result[1]["Gender"] == "Male"
    os.remove("test_data.csv")

    #  Test case when the file does not exist
    with pytest.raises(FileNotFoundError):
        open_file("nonexistent_file.csv")


def test_combine():
    # Test case when both lists have dictionaries with matching names
    list1 = [{'name': 'Alice', 'age': 30}]
    list2 = [{'name': 'Alice', 'gender': 'Female'}]
    result = combine(list1, list2)
    assert result == [{'name': 'Alice', 'age': 30, 'gender': 'Female'}]
    # Test case when both lists have dictionaries with no matching names
    list3 = [{'name': 'Alice', 'age': 30}]
    list4 = [{'name': 'Bob', 'gender': 'Male'}]
    result2 = combine(list3, list4)
    assert result2 == []


def test_check_pn():
    # Test case when multiple matching part numbers are found
    list_dict = [{'part_number': '123', 'full_name': 'Alice'}, {'part_number': '456', 'full_name': 'Bob'}, {'part_number': '123', 'full_name': 'Charlie'}]
    with patch('builtins.input', side_effect=["n", "123", "Cha"]):
        pn = check_pn(list_dict)
        assert pn == {'part_number': '123', 'full_name': 'Charlie'}  # Assuming this is the expected output

    # Test case when no matching part number is found
    list_dict2 = [{'part_number': '123', 'full_name': 'Alice'}, {'part_number': '456', 'full_name': 'Bob'}]
    with patch('builtins.input', side_effect=["n", "555"]):
        with pytest.raises(SystemExit):
            check_pn(list_dict2)

    # Test case when exactly one matching part number is found
    list_dict3 = [{'part_number': '777', 'full_name': 'Alice'}, {'part_number': '456', 'full_name': 'Bob'}]
    with patch('builtins.input', side_effect=["n", "777"]):
        pn = check_pn(list_dict3)
        assert pn == {'part_number': '777', 'full_name': 'Alice'}  # Assuming this is the expected output

def test_check_all_entries():
      # Test case where some values are empty or None
    input_dict = {'key1': 'value1', 'key2': '', 'key3': '', 'key4': 'value4'}

    # Use patch to mock user input
    with patch('builtins.input', side_effect=["y", "555", "y", "new value"]):
        # Call the function
        result = check_all_entries(input_dict)

    # Assert that the result has been updated correctly
    assert result['key2'] == '555'
    assert result['key3'] == 'new value'
    assert result['key1'] == 'value1'
    assert result['key4'] == 'value4'

def test_generate_pdf():
     # Mock user input
    with patch('builtins.input', side_effect=["y", "This document is geneteted by test function"]):
        # Example dictionary for testing
        pdf_data = {
            'full_name': 'John Doe',
            'address': '123 Main St',
            'p/o': 'PO123',
            'o/n': 'ON456',
            'part_number': 'ABC123',
            'rev': 'A',
            'lot': '12345',
            'description': 'This is a test description.',
            'qty_ordered': '10',
            'qty_shipped': '75,890'
        }

        # Call the function
        generate_pdf(pdf_data)

    # Check if the generated PDF file exists
    assert os.path.exists("C_of_C.pdf"), "PDF file was not generated."
