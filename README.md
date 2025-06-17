# SoC-Drone-Attack-Graph

XML to GraphML converter - converts a system description XML file to a yEd compatible GraphML file.
  - parses a structured XML describing components and registers in a system
  - builds a hierarchical graph of System --> Component --> Registers
  - outputs a GraphML file compatible with yEd Graph Editor (https://www.yworks.com/products/yed)

Calculate and display read and write risks for each register, sorted in descending order.
  - risk is calculated using the formula
        Risk = Impact × Vulnerability × Logging Factor
