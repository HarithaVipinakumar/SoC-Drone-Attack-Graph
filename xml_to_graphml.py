import sys
from bs4 import BeautifulSoup as BSS
import codecs

def xml_to_graphml(input_file, output_file):
    print(f"Reading {input_file}")
    with open(input_file, 'r') as file:
        xml = file.read()

    print("Parsing data")
    nodes = []
    edges = []
    node_id_map = {}
    nodes_data = {}
    next_id = 0

    soup = BSS(xml, features="xml")
    system_description = soup.find("SystemDescription")

    root_node = f"System: {system_description['name']}"
    node_id_map[root_node] = next_id
    next_id += 1

    for component in system_description.find_all("Component"):
        comp_name = f"Component: {component['name']}"
        node_id_map[comp_name] = next_id
        next_id += 1
        edges.append((root_node, comp_name))
        
        for register in component.find_all("Register"):
            reg_name = f"Register: {register['name']}"
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

            reg_label = (f"{reg_name}\n"
             f"Read Risk: {read_risk_value:.2f} (Impact: {read_impact}, Vulnerability: {read_vulnerability}, Logging: {read_logging})\n"
             f"Write Risk: {write_risk_value:.2f} (Impact: {write_impact}, Vulnerability: {write_vulnerability}, Logging: {write_logging})")

            node_id_map[reg_label] = next_id
            next_id += 1
            edges.append((comp_name, reg_label))
            
            for access in register.find_all("WriteAccess"):
                for comp in access.find_all("Component"):
                    writer = f"Component: {comp['name']}"
                    if writer in node_id_map:
                        edges.append((writer, reg_label))
            
            for access in register.find_all("ReadAccess"):
                for comp in access.find_all("Component"):
                    reader = f"Component: {comp['name']}"
                    if reader in node_id_map:
                        edges.append((reg_label, reader))
            
            for io in register.find_all("RegisterIO"):
                for inp in io.find_all("Inputs"):
                    for comp in inp.find_all("Component"):
                        input_reg = f"Register: {comp['register']}"
                        if input_reg in node_id_map:
                            edges.append((input_reg, reg_label))
                
                for out in io.find_all("Outputs"):
                    for comp in out.find_all("Component"):
                        output_reg = f"Register: {comp['register']}"
                        if output_reg in node_id_map:
                            edges.append((reg_label, output_reg))

    with codecs.open(output_file, encoding='utf-8', mode='w+') as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" ') 
        f.write('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ') 
        f.write('xmlns:y="http://www.yworks.com/xml/graphml" ') 
        f.write('xmlns:yed="http://www.yworks.com/xml/graphml" ') 
        f.write('xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns ') 
        f.write('http://www.yworks.com/xml/schema/graphml/1.1/ygraphml.xsd">\n')
        f.write('<key for="node" id="d5" yfiles.type="nodegraphics"/>\n')
        f.write('<key attr.name="label" attr.type="string" for="node" id="d4"/>\n')
        f.write('<key attr.name="description" attr.type="string" for="edge" id="d8"/>\n')
        f.write('<key for="edge" id="d9" yfiles.type="edgegraphics"/>\n')
        f.write('<graph id="G" edgedefault="directed">\n')
        
        for node, node_id in node_id_map.items():
            f.write(f'<node id="{node_id}">\n')
            f.write(f'<data key="d4">{node}</data>\n')  # Correct placement for yEd label
            f.write(f'<data key="d5"><y:ShapeNode>\n') # Node appearance
            f.write(f'<y:Geometry height="60.0" width="120.0" x="0.0" y="0.0"/>\n') # Larger node size
            f.write(f'<y:Fill color="#FFFFFF" transparent="false"/>\n')
            f.write(f'<y:BorderStyle color="#000000" type="line" width="1.0"/>\n')
            f.write(f'<y:NodeLabel alignment="center" autoSizePolicy="content" fontFamily="Dialog" fontSize="10" fontStyle="plain" textColor="#000000" visible="true">{node}</y:NodeLabel>\n')
            f.write(f'</y:ShapeNode></data>\n')
            f.write(f'</node>\n')

        for edge in edges:
            source, target = edge
            f.write(f'<edge id="e{next_id}" source="{node_id_map[source]}" target="{node_id_map[target]}">\n')
            f.write(f'<data key="d9"><y:PolyLineEdge>\n')
            f.write(f'<y:Path sx="0.0" sy="15.0" tx="0.0" ty="15.0"/>\n')
            f.write(f'<y:LineStyle color="#000000" type="line" width="1.0"/>\n')
            f.write(f'<y:Arrows source="none" target="standard"/>\n')
            f.write(f'</y:PolyLineEdge></data>\n')
            f.write(f'<data key="d8">Edge from {source} to {target}</data></edge>\n')
            next_id += 1

        f.write('</graph>\n')
        f.write('</graphml>\n')

    print("GraphML file created successfully.")
