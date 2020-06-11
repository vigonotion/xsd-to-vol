import xmltodict
import json
from case_changer import snake_case

def xsd_type_to_type(xsd_type):

    namespace, xtype = xsd_type.split(':')

    if namespace == "xsd":
        p_type = {
            "string": "str",
            "int": "int",
            "long": "int",
            "float": "float",
            "double": "float",
            "boolean": "bool",
            "dateTime": "datetime",
            "date": "datetime",
            "anyURI": "Url"
        }.get(xtype)

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
print("from voluptuous import In, Schema, Url")
print()


"""
Simple types are like enums or like voluptuous In().
"""

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

    print(f"\"\"\"\n{name}\n\n{docs}\n\"\"\"")
    print(f"{name} = {simple_schema(vals)}")

    print("\n\n")


"""
Complex types.
"""

def complex_schema(complex_type):
    S = []
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
            name = element["@name"]
            doc = element["xsd:annotation"]["xsd:documentation"] if "xsd:annotation" in element else ""
            e_type = xsd_type_to_type(element["@type"])

            if "default" in element:
                doc += f"\nDefault: {element['@default']}"

            #docs += (f"{name}: {e_type} {doc}\n")

            S.append(f"\"{name}\": {e_type}")
    
    #print(f"{docs}\"\"\"")

    if "xsd:complexContent" in complex_type:
        base = xsd_type_to_type(complex_type["xsd:complexContent"]["xsd:extension"]["@base"])
        s = "{" + ", ".join(S) + "}"
        return f"Schema.extend({base}, {s})"

    return "Schema({" + ", ".join(S) + "})"

for complex_type in schema["xsd:schema"]["xsd:complexType"]:
    type_name = complex_type["@name"]
    docs = complex_type.get("xsd:annotation", {}).get("xsd:documentation", "")
    if docs != "":
        docs += "\n\n"

    print(f"\"\"\"\n{type_name}\n\"\"\"")

    s = complex_schema(complex_type)

    print(f"{type_name} = {s}")

    print("\n\n")



"""
Elements.
"""

for element_type in schema["xsd:schema"]["xsd:element"]:
    type_name = element_type["@name"]
    docs = element_type.get("xsd:annotation", {}).get("xsd:documentation", "")
    if docs != "":
        docs += "\n\n"

    print(f"\"\"\"\n{type_name}\n\"\"\"")

    # more docs

    #print(f"\"\"\"\n")

    if "xsd:complexType" in element_type:
        print(complex_schema(element_type["xsd:complexType"]))
    else:
        raise Exception("No complexType!")
    

    print("\n\n")
