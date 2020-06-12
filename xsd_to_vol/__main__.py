import argparse

from xsd_to_vol import xsd_to_vol

def main():

    parser = argparse.ArgumentParser(description='Convert XML Schema Definitions to Voluptuous schemas.')

    parser.add_argument('-i', '--input-file', help='xml schema definition file. If empty, stdin is used.')
    parser.add_argument('-o', '--output-file', help='filename for the generated .py file containing the voluptuous schemas. If empty, prints to stdout.')

    args = parser.parse_args()

    if args.input_file is not None:
        with open(args.input_file, 'r') as schema_file:
            xsd = schema_file.read()
    else:
        import sys

        if not sys.stdin.isatty():
            xsd = "".join(sys.stdin.readlines()).replace('\n', '')
    

    vol = xsd_to_vol(xsd)

    if args.output_file is not None:
        with open(args.output_file, 'w') as vol_file:
            vol_file.write(vol)
    else:
        print(vol)