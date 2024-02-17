from fpdf import FPDF
import sys
import csv
from tabulate import tabulate
from datetime import date


class PDF(FPDF):
    def header(self):
        """Method to create the header section of the PDF."""
        # Rendering logo:
        self.image(
            "/workspaces/107325954/CS50Python/project/Logo_ small.png", 15, 10, 33
        )
        # Setting font: times
        self.set_font("times", size=10)
        # Moving cursor to the right:
        self.cell(30)
        XPos = {"LMARGIN": 60}  # Define X positions
        YPos = {"NEXT": 7}  # Define Y positions
        #  # Add address lines
        self.set_xy(XPos["LMARGIN"], YPos["NEXT"])
        self.cell(0, 4, "461 Timpson Pl, Bronx, NY 10455")
        # Moving cursor to the right:
        self.set_x(self.get_x() + 40)
        YPos["NEXT"] += 5
        self.set_xy(XPos["LMARGIN"], YPos["NEXT"])
        self.cell(0, 4, "Tel:         (718) 401-0288      Fax:    (718) 401-0663")
        # Moving cursor to the right:
        self.set_x(self.get_x() + 40)
        YPos["NEXT"] += 4
        self.set_xy(XPos["LMARGIN"], YPos["NEXT"])
        self.cell( 0, 4, "Email:     quality@roanwellcorp.com",)
        # Moving cursor to the right:
        self.set_x(self.get_x() + 40)
        YPos["NEXT"] += 4
        self.set_xy(XPos["LMARGIN"], YPos["NEXT"])
        self.cell(0, 4, "Web:       www.roanwell.com")
        # Line break
        self.ln(10)
        # Performing a line break:
        self.ln(20)

        # draw line
        self.set_line_width(0.4)  # set line thickmess
        self.line(10, 25, 200, 25)

    def footer(self):
        """Method to create the footer section of the PDF"""
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-30)
        self.line(10, 264, 200, 264)
        self.set_font("times", size=12)
        self.cell(0, 4, "IF ANY FURTHER ASSISTANCE IS REQUIRED, PLEASE DO NOT HESITATE TO CONTACT US",
            align="C",
        )
        self.line(10, 274, 200, 274)
        self.ln(7)
        # Setting font:
        self.set_font("times", size=6)
        self.cell(0, 4, "Form: QF 20-01", align="L")
        text_width = self.get_string_width("Rev 11 (7-26-2022)")
        # Calculate the X coordinate to center the text
        x_coordinate = (self.w - text_width) / 2
        # Move the cursor to the calculated X coordinate
        self.set_x(x_coordinate)
        # Add the centered text
        self.cell(0, 4, "Rev 11 (7-26-2022)", align="L")
        self.ln(5)
        self.set_font("times", "I", size=10)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

        # Performing a line break:
        self.ln(4)


def main():

    # Open and read the first CSV file to get address information
    list = open_file("PT_Address.csv")

    # Initialize an empty list to store selected addresses and a set to keep track of added names
    selected_addresses = []
    added_names = set()

    # Iterate over the original list of dictionaries
    for item in list:
        # Extract desired elements from each dictionary
        name = item['AddressSource']
        # Check if the name has already been added
        if name not in added_names:
            # Add the item to the selected list
            selected_item = {
                'name': item['AddressSource'],
                'full_name': item['AddressName'],
                'address': f"{item['Line1']}, {item['City']}, {item['State']}, {item['PostalCode']}",
            }
            # Add the name to the set of added names
            added_names.add(name)
            # Append the selected item to the list of selected addresses
            selected_addresses.append(selected_item)

    # Open and read the second CSV file to get inspection information
    list2 =open_file("PT_Inspection.csv")
    final_inspection=[]

    # Iterate over the list of dictionaries from the second CSV file
    for item in list2:
        # Check if the inspection type is 'Final'
        inspection = item['InspectionSpecification_type']
        if inspection == 'Final':
            # Create a selected item with required data
            selected_item = {
                'name': item['Customer'],
                'part_number': item['Part'],
                'rev': item['PartRevision'],
                'lot': item['Lot'],
                'description': item['PartDescription'],
                'p/o': item['PO'],
                'o/n': item['SO'],
                'qty_ordered': item['TotalQuantity'],
                'qty_shipped':"" # Initialize qty_shipped with an empty string
            }
            # Append the selected item to the list of final inspections
            final_inspection.append(selected_item)

    # Combine the lists of final inspections and selected addresses
    c_of_c_data= combine (final_inspection,selected_addresses,)

    # Print the number of entries in the inspection record marked as "Final"
    print(f"There ara {len(c_of_c_data)} entry in inspection record marked as \"Final\"")

    # Check the part number and select relevant information for generating the Certificate of Conformance (C of C)
    choosen_pn=check_pn(c_of_c_data)

    # Check for empty fields in the selected information and prompt for new values if necessary
    check_all_entries(choosen_pn)

    # Print a snapshot of the entered information using tabulate
    print (f"Here is snapshot of entered information:")
    choosen_list=[choosen_pn]
    print(tabulate(choosen_list, headers="keys", tablefmt="grid"))

    # Prompt the user to generate a PDF file with the information
    generate_cofc=input("Do you want to generate PDF file with this information? ")
    if generate_cofc.lower() == "yes" or generate_cofc.lower() == "y":
        # Generate the PDF file with the selected information
        generate_pdf(choosen_pn)
    else:
        # Exit the program if the user chooses not to generate the PDF file
        sys.exit("Program exit")


def check_all_entries(dict):
    """Checks all keys in a dictionary for empty or None values
     and prompts the user to assign new values if necessary."""

    # Iterate over all keys in the dictionary
    for key in dict:
        # Check if the value for the current key is empty or None
        if not dict[key]:
            print("")
            print(f"The value for key '{key}' is empty or None.")
            new_data=input(f"Do you want to assign new value for '{key}'?. Answer 'y/n': ")
            if check_answer(new_data):
                new_value=input("Enter new value here: ")
                dict[key]=new_value

    return dict


def check_pn(list_dict):
    """Allows the user to select a part number for Certificate of Conformance (C of C) generation."""

    # Initialize empty lists to store selected part numbers
    choosen_pn=[]
    choosen_pn2=[]
    # Prompt the user to see a list of part numbers that passed final inspection
    promt1= input("Do you want to see list of part numbers that are passed final inspection? ")
    if check_answer(promt1):
        for item in list_dict:
            print(item['part_number'])

    # Prompt the user to enter a part number for C of C generation
    pn=input("Enter part number for C of C generation: ")
    print(pn)

    # Find the selected part number in the list of dictionaries
    for item in list_dict:
        if pn==item['part_number']:
            choosen_pn.append(item)

    # Handle cases where no matching part number is found
    if len(choosen_pn)==0:
            sys.exit("There is no information for entered part number")
    # Handle cases where exactly one matching part number is found
    elif len(choosen_pn)==1:
        return choosen_pn[0]
    # Handle cases where multiple matching part numbers are found
    else:
        print("____________________________________")
        print("")
        print (f"There are {len(choosen_pn)} entries for this part number. Here are the customer's names: ")
        print("____________________________________")
        print("")
        for item in choosen_pn:
            print(item['full_name'])
        print("____________________________________")

        # Prompt the user to enter the first three or more letters of the customer's name
        choosen=input("Please enter the first three or more letters of the name you want to proceed: ")
        while len(choosen)<3:
            print("There are fewer than 3 letters entered.")
            choosen=input("Please enter the first three or more letters of the name you want to proceed: ")

        # Find part numbers matching the entered customer's name
        for item in choosen_pn:
            if item['full_name'].lower().startswith(choosen.lower()):
                choosen_pn2.append(item)

        #  Handle cases where multiple part numbers match the entered customer's name
        if len(choosen_pn2) >1:
            print("")
            print("There are more than one entry with the same part number for the same customer.")
            print("____________________________________")
            print("You will be prompted to enter 'KEY' data manually.")
            print("____________________________________")
             # Clear certain fields in the first matching entry
            choosen_pn2[0]['p/o']=""
            choosen_pn2[0]['o/n']=""
            choosen_pn2[0]['qty_ordered']=""

            return choosen_pn2 [0]
        # Handle cases where no matching part numbers are found
        elif  len(choosen_pn2) ==0:
            sys.exit("There are no entry that mach you input")
        # Handle cases where exactly one matching part number is found
        else:
            return choosen_pn2 [0]


def combine(list1, list2):
    """Combines dictionaries from two lists based on a common key and returns a new list"""

    # Initialize an empty list to store the combined dictionaries
    combined_list = []
    # Iterate over each dictionary in list1
    for item1 in list1:
        # Find matching item in list2 based on the "name" key
        for item2 in list2:
            # Check if there's a match based on the value of the "name" key
            if item1['name'] == item2['name']:
                # Combine dictionaries and add to the combined list
                combined_dict = {**item1, **item2}
                combined_list.append(combined_dict)
                break  # Stop searching in list2 after finding a match

    # Return the list of combined dictionaries
    return combined_list


def open_file(data):
    """ Opens a CSV file and reads its contents into a list of dictionaries."""

    # Initialize an empty list to store the data
    list = []
    try:
        # Attempt to open the CSV file
        with open(data) as file:
            # Create a CSV reader object using csv.DictReader to read the file
            reader = csv.DictReader(file)

            # Iterate over each line in the CSV file
            for line in reader:
                # Append each line (represented as a dictionary) to the data_list
                list.append(line)

    except FileNotFoundError:
        # If the file is not found, raise FileNotFoundError
        raise FileNotFoundError("The file could not be found.")

    # Return the list of dictionaries containing the data from the CSV file
    return list


def generate_pdf(dict):
    """Generete PDF file based on information by paased dict"""

     # Get today's date and convert it to string in date format
    today_day = date.today().strftime('%Y-%m-%d')

    # Initialize a new PDF object
    pdf = PDF()
    pdf.add_page()
    pdf.set_y(30)
    pdf.set_font("times", "BU", size=14)
    pdf.cell(0, 5, "CERTIFICATE OF CONFORMANCE", align="C")

    # Set up multiline text
    pdf.set_y(35)
    pdf.set_font("times", "B", size=12)
    text1 = """THIS IS TO CERTIFY THAT THE FOLLOWING PRODUCTS AND/OR MATERIALS LISTED WERE PRODUCED, INSPECTED AND ACCEPTED IN ACCORDANCE WITH APPLICABLE DRAWINGS AND/OR SPECIFICATIONS. ALL RELATED RECORDS ARE ON FILE AND MAY BE REVIEWED UPON TIMELY REQUEST."""
    text2 = """NO COUNTERFEIT MATERIALS, PARTS OR COMPONENTS CONSTITUTE IN ANY PORTION THE CONTENTS OF THE PRODUCT(S) DESCRIBED BELOW."""
    # Write text
    pdf.ln(5)
    pdf.multi_cell(0, 5.25, text1)
    pdf.ln(1)
    pdf.multi_cell(0, 5.25, text2)

    # Define positions and dimensions for various elements
    XPos = {"LMARGIN": 15}  # Define X positions
    YPos = {"NEXT": 80}  # Define Y positions
    prt_num_l=43
    rev_l=14
    lot_l=24
    descrp_l=54
    costumer_l=prt_num_l+rev_l+lot_l+descrp_l
    ordered_l=22.5
    shipped_l=22.5

    # Add customer details
    pdf.set_font('times', 'B', 12)
    pdf.set_xy(XPos["LMARGIN"], YPos["NEXT"])
    pdf.cell(costumer_l, 15, dict['full_name'], 0, align='L')
    # For Row 2 Text
    pdf.set_font('times', '', 12)
    pdf.set_xy(XPos["LMARGIN"], YPos["NEXT"]+10)
    pdf.cell(costumer_l, 15, dict['address'], 0, align='L')
    # Create empty cell
    pdf.set_xy(XPos["LMARGIN"], YPos["NEXT"])
    pdf.cell(costumer_l, 30, '', 1, align='C')

    # Add order details
    pdf.set_font('times', 'B', 12)
    #DATE
    pdf.set_xy(XPos["LMARGIN"] + costumer_l, YPos["NEXT"])
    pdf.cell(ordered_l, 10, 'DATE:', 1, align='R')
    #PO
    pdf.set_xy(XPos["LMARGIN"] + costumer_l, YPos["NEXT"]+10)
    pdf.cell(ordered_l, 10, 'PO:', 1, align='R')
    #O/N
    pdf.set_xy(XPos["LMARGIN"] + costumer_l, YPos["NEXT"]+20)
    pdf.cell(ordered_l, 10, 'O/N:', 1, align='R')

    pdf.set_font('times', '', 12)
    pdf.set_xy(XPos["LMARGIN"] + costumer_l+ordered_l, YPos["NEXT"])
    pdf.cell(shipped_l, 10, today_day, 1, align='L')
    pdf.set_xy(XPos["LMARGIN"] + costumer_l+ordered_l, YPos["NEXT"]+10)
    pdf.cell(shipped_l, 10, dict['p/o'], 1, align='L')
    pdf.set_xy(XPos["LMARGIN"] + costumer_l+ordered_l, YPos["NEXT"]+20)
    pdf.cell(shipped_l, 10, dict['o/n'], 1, align='L')

    # Add headers for the item
    pdf.set_font('times', 'B', 12)
    # For 'PART'
    pdf.set_xy(XPos["LMARGIN"], YPos["NEXT"]+32.5)
    pdf.cell(prt_num_l, 10, 'PART',  align='C')
    # For 'NUMBER'
    pdf.set_xy(XPos["LMARGIN"], YPos["NEXT"]+37.5)
    pdf.cell(prt_num_l, 10, 'NUMBER',  align='C')
    # Create empty cell
    pdf.set_xy(XPos["LMARGIN"], YPos["NEXT"]+30)
    pdf.cell(prt_num_l, 20, '', 1, align='C')
    #REV
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l, YPos["NEXT"]+30)
    pdf.cell(rev_l, 20, 'REV', 1, align='C')
    #LOT
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l, YPos["NEXT"]+30)
    pdf.cell(lot_l, 20, 'LOT', 1, align='C')
    #ITEM DESCRIPTION
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l, YPos["NEXT"]+30)
    pdf.cell(descrp_l, 20, 'ITEM DESCRIPTION', 1, align='C')
    # For 'QTY'
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l+descrp_l, YPos["NEXT"]+32.5)
    pdf.cell(ordered_l, 10, 'QTY',  align='C')
    # For 'ORDERED'
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l+descrp_l, YPos["NEXT"]+37.5)
    pdf.cell(ordered_l, 10, 'ORDERED',  align='C')
    # Create empty cell
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l+descrp_l, YPos["NEXT"]+30)
    pdf.cell(ordered_l, 20, '', 1, align='C')
    # For 'QTY'
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l+descrp_l+ordered_l, YPos["NEXT"]+32.5)
    pdf.cell(shipped_l, 10, 'QTY',  align='C')
    # For 'SHIPPED'
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l+descrp_l+ordered_l, YPos["NEXT"]+37.5)
    pdf.cell(shipped_l, 10, 'SHIPPED',  align='C')
    # Create empty cell
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l+descrp_l+ordered_l, YPos["NEXT"]+30)
    pdf.cell(shipped_l, 20, '', 1, align='C')


    # Add item details
    pdf.set_font('times', '', 12)
    pdf.set_xy(XPos["LMARGIN"], YPos["NEXT"]+30+20)
    pdf.cell(prt_num_l, 60, dict['part_number'], 1, align='C')

    pdf.set_xy(XPos["LMARGIN"]+prt_num_l, YPos["NEXT"]+30+20)
    pdf.cell(rev_l, 60, dict['rev'], 1, align='C')

    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l, YPos["NEXT"]+30+20)
    pdf.cell(lot_l, 60, dict['lot'], 1, align='C')

    # Add item description
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l, YPos["NEXT"]+30+20)
    pdf.cell(descrp_l, 60, '', 1, align='C')

    text = dict['description']

    text_list=split_string(text, 20)
    count = 0
    space =0
    for element in text_list:
        pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l, YPos["NEXT"]+30+space)
        pdf.cell(descrp_l, 60, f"{element}", 0, align='L')
        space +=7
        count +=1
        if count >=7 :
            break

    # Add ordered and shipped quantities
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l+ descrp_l, YPos["NEXT"]+30+20)
    pdf.cell(ordered_l, 60, dict['qty_ordered'], 1, align='C')
    pdf.set_xy(XPos["LMARGIN"]+prt_num_l+rev_l+lot_l+ descrp_l+ordered_l, YPos["NEXT"]+30+20)
    pdf.cell(shipped_l, 60, dict['qty_shipped'], 1, align='C')

    # Add notes if requested
    note=input("Do you want to add any notes? ")
    if check_answer(note):
        note_text= input("Enter your NOTE: ")
        note_list=split_string(note_text, 81)
        pdf.set_font('times', '', 12)
        pdf.set_xy(XPos["LMARGIN"], YPos["NEXT"]+30+20+60)
        pdf.cell(25, 10, "NOTE:", 0, align='L')
        sp =0
        for element in note_list:
            pdf.set_xy(XPos["LMARGIN"]+15, YPos["NEXT"]+30+20+60+sp)
            pdf.cell(81, 10, f"{element}", 0, align='L')
            sp +=7

    # Add approval information
    pdf.set_font('times', 'B', 12)
    pdf.set_xy(XPos["LMARGIN"]+5, YPos["NEXT"]+30+20+80)
    pdf.cell(25, 60, 'APPROVED BY', 0, align='L')
    pdf.line(55, 241.5, 155, 241.5)
    pdf.set_xy(XPos["LMARGIN"]+142.5, YPos["NEXT"]+30+20+80)
    pdf.cell(25, 60, today_day, 0, align='L')

    # Save PDF to file
    pdf.output("C_of_C.pdf")


def check_answer(responce):
    # Checks if the response provided by the user indicates a positive answer (yes or y).
    return responce.lower() == "yes" or responce.lower() == "y"

def split_string(input_str, max):
    # Split the input string into words
    words = input_str.split()

    # Initialize variables
    new_strings = []
    current_string = ''

    # Iterate over the words
    for word in words:
        # Check if adding the word exceeds max characters
        if len(current_string) + len(word) + 1 <= max:
            # Add the word to the current string
            if current_string:
                current_string += ' '
            current_string += word
        else:
            # Add the current string to the list and start a new string
            new_strings.append(current_string)
            current_string = word

    # Add the last string to the list
    if current_string:
        new_strings.append(current_string)

    return new_strings

if __name__ == "__main__":
    main()
