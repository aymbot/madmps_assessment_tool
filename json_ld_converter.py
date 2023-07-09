import json
from pyld import jsonld
from rdflib import Graph
import os

# Load the JSON-LD context file
context_folder = 'mappings' 
context_file_path = os.path.join(context_folder, 'dcso.jsonld')
with open(context_file_path, 'r') as context_file:
    context = json.load(context_file)

# Load the OWL ontology file using rdflib
ontology_folder = 'mappings'
ontology_file_path = os.path.join(ontology_folder, 'dcso.ttl')
graph = Graph()
graph.parse(ontology_file_path, format='turtle')

# Convert the ontology to JSON-LD format
json_ld_data = graph.serialize(format='json-ld', context=context)

madmps = []

folder_path = 'madmps'

for filename in ['madmp1.json', 'madmp2.json', 'madmp3.json', 'madmp4.json', 'madmp5.json']:
    try:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            madmp = json.load(file)
            madmps.append(madmp)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {filename}")
        print(f"JSONDecodeError: {e}")
    except FileNotFoundError as e:
        print(f"File not found: {filename}")
        print(f"Error: {e}")

# Add the JSON-LD context to the maDMPs
for madmp in madmps:
    madmp["@context"] = context

# Convert the maDMPs to JSON-LD using pyld and save in 'output' folder
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

for i, madmp in enumerate(madmps):
    try:
        expanded = jsonld.expand(madmp)
        framed = jsonld.frame(expanded, context)
        json_ld_data = json.dumps(framed, indent=2)

        output_file = os.path.join(output_folder, f'madmp{i+1}.jsonld')
        with open(output_file, 'w') as output:
            output.write(json_ld_data)

        print(f'Saved JSON-LD data for maDMP{i+1} to {output_file}')
    except Exception as e:
        print(f"Error converting maDMP to JSON-LD: maDMP{i+1}")
        print(f"Exception: {e}")
