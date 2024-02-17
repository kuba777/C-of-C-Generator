# Certificate of Conformance Generator
#### Video Demo: 
## Project Overview:
The project is a Python script designed to generate a Certificate of Conformance (C of C) in PDF format based on information obtained from two CSV files containing address and inspection data. The C of C includes customer details, order information, item descriptions, and approval sections. The script is interactive, allowing users to input part numbers, select customer names, and add additional notes as needed.

### Features:

* **Input Data:** Reads address and inspection information from CSV files.

* **Certificate Generation:** Generates a C of C PDF based on selected part numbers and customer details.

* **Interactive:** Prompts users for input such as part numbers and additional notes.

* **Flexible:** Handles cases where multiple items match the entered criteria.

* **Customizable:** Users can specify desired lengths for part numbers, revisions, lots, descriptions, and customer names.


### Installation
Install Python 3.x from the official website: <https://www.python.org/>

Install required libraries using pip:

```pip install fpdf2```

```pip install tabulate```

```pip install pytest```

### Usage
1. Place the CSV files containing address and inspection data in the same directory as the script.
2. Run the script using Python:

    ```python project.py```

3.  Follow the prompts to select part numbers, enter additional notes, and generate the PDF.

### Notes
Make sure the CSV files are properly formatted with headers.
Ensure the logo file (Logo_small.png) is accessible from the script.

### File Structure:
**1.&nbsp;  project.py:** &nbsp;&nbsp;&nbsp;&nbsp; This is the main Python script for the project. It contains functions to read data from CSV files, generate a PDF based on the data, handle user interactions, and combine data from different sources. The script utilizes the fpdf library to create PDF documents and the tabulate library for formatting tabular data. Key functions include:
*   ```main():``` The main function that orchestrates the entire process of generating the C of C.
*   ```check_all_entries(dict):``` Function to check if any entries in a dictionary are empty and prompt the user to provide values.
*   ```check_pn(list_dict):``` Function to allow the user to select a part number for generating the C of C.
*   ```combine(list1, list2):``` Function to combine dictionaries from two lists based on a common key.
*   ```open_file(data):``` Function to open and read data from a CSV file into a list of dictionaries.
*   ```generate_pdf(dict):``` Function to generate the PDF document based on the selected data.

**2.&nbsp;    test_project.py:** &nbsp;&nbsp;&nbsp;&nbsp; contains a series of test cases for each function in the **project.py** script. These tests ensure that each function behaves as expected under various conditions, validating the functionality and reliability of the project's code. It include:
*   ```test_check_answer():```  Tests the check_answer() function, which checks if the user's response indicates a positive answer (yes or y).
*   ```test_split_string():```  Tests the split_string() function, which splits a string into substrings based on a maximum length.
*   ```test_open_file():``` Tests the open_file() function, which opens and reads data from a CSV file into a list of dictionaries.
*   ```test_combine():```   Tests the combine() function, which combines dictionaries from two lists based on a common key. Includes test cases for when both lists have matching names and when they don't.
*   ```test_check_pn():```  Tests the check_pn() function, which allows the user to select a part number for generating the Certificate of Conformance (C of C). Includes test cases for when multiple matching part numbers are found, no matching part number is found, and exactly one matching part number is found.
*   ```test_check_all_entries():``` Tests the check_all_entries() function, which checks all keys in a dictionary for empty or None values and prompts the user to assign new values if necessary.
*   ```test_generate_pdf():```  Tests the generate_pdf() function, which generates a PDF file based on the information passed to it. Includes mock user input to simulate user interaction. Checks if the PDF file is generated successfully.

**3.&nbsp;    Logo_small.png:** &nbsp;&nbsp;&nbsp;&nbsp;    This is an image file used as the logo in the header section of the generated PDF. The script includes a reference to this image file to display it in the PDF header.

**4.&nbsp;    PT_Address.csv:** &nbsp;&nbsp;&nbsp;&nbsp;    This is a sample CSV file containing address data. It includes colums related to customer adderess, such as AddressSource, AddressName, Line1 (addres itself), City, State, and PostalCode.

**5.&nbsp;    PT_Inspection.csv:** &nbsp;&nbsp;&nbsp;&nbsp; This is a sample CSV file containing inspection data.
It includes columns such as InspectionSpecification_type, Customer, Part, PartRevision, Lot, PartDescription, PO, SO, and TotalQuantity.

**6.&nbsp;    requirements.txt:** &nbsp;&nbsp;&nbsp;&nbsp;  pip-installable libraries that project requires are listed here.

**7.&nbsp;    README.md:** &nbsp;&nbsp;&nbsp;&nbsp; A file that describes this project.


### Summary:
The project files collectively enable the generation of a C of C PDF document by processing address and inspection data from CSV files. The Python script orchestrates the entire process, from reading data to user interactions and PDF generation, making it a convenient tool for generating certificates in a manufacturing or quality assurance context.
