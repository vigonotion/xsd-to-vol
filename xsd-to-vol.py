import xmltodict
import json
from case_changer import snake_case

class Schema:
    def __init__(self, name, schema, documentation, requirements):
        self.name = name
        self.schema = schema
        self.documentation = documentation
        self.requirements = requirements

    def __str__(self):
        return f"\"\"\"{self.name}\n\n{self.documentation}\n\"\"\"\n\n{self.name} = {self.schema}"

preset_types = {
            "string": "str",
            "int": "int",
            "long": "int",
            "float": "float",
            "double": "float",
            "boolean": "bool",
            "dateTime": "DateTime",
            "date": "DateTime",
            "anyURI": "Url"
        }

def xsd_type_to_type(xsd_type):

    namespace, xtype = xsd_type.split(':')

    if namespace == "xsd":
        p_type = preset_types.get(xtype)

        if not p_type:
            raise Exception("Type %s not supported" % xtype)

        return p_type

    return xtype

with open('schema.xsd', 'r') as schema_file:
  schema_xml = schema_file.read()
  schema = xmltodict.parse(schema_xml)

#print(json.dumps(schema, indent=2))

"""
Header.
"""
print("from voluptuous import In, Schema, Url\nfrom datetime import datetime\nimport pytz")
print()

print("""
def DateTime(dt):
    dt = pytz.utc.localize(dt)
    return f"{dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}{dt.strftime('%z')}"
""")

print()

"""
Simple types are like enums or like voluptuous In().
"""

Schemas = []

def simple_schema(values):
    return f"In([{', '.join(vals)}])"

for simple_type in schema["xsd:schema"]["xsd:simpleType"]:
    name = simple_type["@name"]
    docs = simple_type["xsd:annotation"]["xsd:documentation"].replace("\t\t\t\t", "")

    enum = simple_type["xsd:restriction"]["xsd:enumeration"]

    if isinstance(enum, list):
        vals = [f"\"{x['@value']}\"" for x in enum]
    else:
        vals = [f"\"{enum['@value']}\""]


    Schemas.append(Schema(name, simple_schema(vals), docs, []))



"""
Complex types.
"""

def complex_schema(name, complex_type, docs):
    S = []
    R = [] # required types
    sequence = None

    if "xsd:sequence" in complex_type:
        sequence = complex_type["xsd:sequence"]
    elif "xsd:complexContent" in complex_type and "xsd:sequence" in complex_type["xsd:complexContent"]:
        sequence = complex_type["xsd:complexContent"]["xsd:sequence"]
    elif "xsd:complexContent" in complex_type \
        and "xsd:extension" in complex_type["xsd:complexContent"] \
        and "xsd:sequence" in complex_type["xsd:complexContent"]["xsd:extension"]:
        sequence = complex_type["xsd:complexContent"]["xsd:extension"]["xsd:sequence"]
    
    if sequence:
        for element in sequence["xsd:element"] if isinstance(sequence["xsd:element"], list) else [sequence["xsd:element"]]:
            e_name = element["@name"]
            doc = element["xsd:annotation"]["xsd:documentation"] if "xsd:annotation" in element else ""

            min_occurs = element.get("@minOccurs", "unbounded")
            max_occurs = element.get("@maxOccurs", "unbounded")

            e_type = xsd_type_to_type(element["@type"])

            if "default" in element:
                doc += f"\nDefault: {element['@default']}"

            docs += (f"{e_name}: {e_type} {doc} ({min_occurs} - {max_occurs})\n")

            S.append(f"\"{e_name}\": {e_type}")

            if e_type not in preset_types.values():
                R.append(e_type)
    
    #print(f"{docs}\"\"\"")

    if "xsd:complexContent" in complex_type:
        base = xsd_type_to_type(complex_type["xsd:complexContent"]["xsd:extension"]["@base"])
        s = "{" + ", ".join(S) + "}"
        schema = f"Schema.extend({base}, {s})"

    schema = "Schema({" + ", ".join(S) + "})"

    return Schema(name, schema, docs, list(set(R)))

for complex_type in schema["xsd:schema"]["xsd:complexType"]:
    name = complex_type["@name"]
    docs = complex_type.get("xsd:annotation", {}).get("xsd:documentation", "")
    if docs != "":
        docs += "\n\n"


    s = complex_schema(name, complex_type, docs)

    Schemas.append(s)




"""
Elements.
"""

for element_type in schema["xsd:schema"]["xsd:element"]:
    type_name = element_type["@name"]
    docs = element_type.get("xsd:annotation", {}).get("xsd:documentation", "")
    if docs != "":
        docs += "\n\n"

    if "xsd:complexType" in element_type:
        Schemas.append(complex_schema(name, element_type["xsd:complexType"], docs))
    else:
        raise Exception("No complexType!")
    


"""
Print schemas in correct order (using Kahn's algorithm).
"""

L = []
S = [x for x in Schemas if len(x.requirements) == 0]

while len(S) > 0:
    n = S.pop()
    
    L.append(n)

    for m in [x for x in Schemas if n.name in x.requirements]:
        m.requirements.remove(n.name)


        if len(m.requirements) == 0:
            S.append(m)

for s in L:
    print(s)
    print("\n\n")