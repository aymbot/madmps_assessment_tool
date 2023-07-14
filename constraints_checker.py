import rdflib
import pyshacl
import os

output_folder = 'output'

# Load the SHACL shapes graph
shapes_graph = rdflib.Graph()
shapes_graph.parse('shacl_constraints\shapes_6b2.ttl', format='turtle')

# Perform SHACL validation for each madmp file
for i in range(1, 12):
    filename = os.path.join(output_folder, f"madmp{i}.jsonld")
    if os.path.isfile(filename):
        print(f"Checking madmp: {filename}")
        madmp_graph = rdflib.Graph().parse(filename, format='json-ld')
        conforms, results_graph, results_text = pyshacl.validate(madmp_graph, shacl_graph=shapes_graph)
        print(f"Validation conforms: {conforms}")
        print(f"Validation results:\n{results_text}")
        print("=" * 50)
