from bs4 import BeautifulSoup as BSS

def calculate_and_sort_risks(input_file):
    print(f"Reading {input_file}")
    with open(input_file, 'r') as file:
        xml = file.read()

    print("Parsing data")
    registers_with_risk = []

    soup = BSS(xml, features="xml")
    system_description = soup.find("SystemDescription")

    for component in system_description.find_all("Component"):
        comp_name = component['name']
        
        for register in component.find_all("Register"):
            reg_name = register['name']
            read_risk = register.find("ReadRisk")
            write_risk = register.find("WriteRisk")
            
            read_impact = int(read_risk['Impact'])
            read_vulnerability = int(read_risk['Vulnerability'])
            read_logging = float(read_risk['Logging'])
            read_risk_value = read_impact * read_vulnerability * read_logging

            write_impact = int(write_risk['Impact'])
            write_vulnerability = int(write_risk['Vulnerability'])
            write_logging = float(write_risk['Logging'])
            write_risk_value = write_impact * write_vulnerability * write_logging

            registers_with_risk.append({
                'reg_name': reg_name,
                'read_risk': read_risk_value,
                'write_risk': write_risk_value
            })

    sorted_registers_by_read = sorted(registers_with_risk, key=lambda x: x['read_risk'], reverse=True)
    sorted_registers_by_write = sorted(registers_with_risk, key=lambda x: x['write_risk'], reverse=True)

    print("Sorted by Read Risk (Descending):")
    for reg in sorted_registers_by_read:
        print(f"Register: {reg['reg_name']} - Read Risk: {reg['read_risk']:.2f}")

    print("\nSorted by Write Risk (Descending):")
    for reg in sorted_registers_by_write:
        print(f"Register: {reg['reg_name']} - Write Risk: {reg['write_risk']:.2f}")

# Call the function with your XML input file
# calculate_and_sort_risks('your_input_file.xml')
