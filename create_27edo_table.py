#!/usr/bin/env python3
"""Generate 27-EDO HTML table"""

from functional_harmony import parse_edo_data_file, generate_html_table

# Parse the EDO data file to load all systems
edo_systems = parse_edo_data_file('edo_data.md')

# Generate HTML table for 27-EDO
if 27 in edo_systems:
    system = edo_systems[27]
    filename = '27edo_table.html'
    generate_html_table(system, filename)
    print(f"Generated {filename}")
else:
    print("27-EDO system not found in edo_data.md")
