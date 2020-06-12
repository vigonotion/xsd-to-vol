# xsd-to-vol


![ci](https://github.com/vigonotion/xsd-to-vol/workflows/ci/badge.svg)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://github.com/vigonotion/xsd-to-vol/issues"><img alt="Open Issues" src="https://img.shields.io/github/issues/vigonotion/xsd-to-vol"></a>
<a href="https://github.com/vigonotion/xsd-to-vol/releases"><img alt="Release" src="https://img.shields.io/github/release/vigonotion/xsd-to-vol"></a>
[![PyPI version](https://badge.fury.io/py/xsd-to-vol.svg)](https://badge.fury.io/py/xsd-to-vol)

Convert XML Schema Definition files to voluptuous schemas.

Get it on PyPi:
```sh
pip install xsd-to-vol
```

## Binary file usage

Basic usage:

```sh
xml-to-vol -i schema.xsd -o schema.py
```

Basic pipe usage:

```sh
cat schema.xsd | xml-to-vol > schema.py
```

Pipe through black formatter:

```sh
cat schema.xsd | xsd-to-vol | black - > schema.py
```

Advanced piping example with curl:

```sh
curl -s https://api-test.geofox.de/gti/public/geofoxThinInterfacePublic.xsd 2>&1 | xsd-to-vol | black - > schema.py
```

You can also mix input/output files and stdin/stdout.

## Library usage

You can also use the `xml_to_vol` method to convert your schema:

```python
from xsd_to_vol import xsd_to_vol

with open("schema.xsd", 'r') as schema_file:
    xsd = schema_file.read()
    print(xsd_to_vol(xsd))
```

## To Do

While the generation should work for most xsd files, there are some features I'd
like to have in future versions:

- [ ] Only include used imports: Currently all possible voluptuous requirements
        are imported. The required imports can be determined.
- [ ] Tests: Gather different xsd schemas and build pytests to test the generation.
- [ ] Automatic code formatting: Run black over the code (without piping).

## Contributions are welcome!

If you want to contribute to this, please read the [Contribution guidelines](CONTRIBUTING.md)
