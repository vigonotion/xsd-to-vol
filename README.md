# xsd-to-vol

Convert XML Schema Definition files to voluptuous schemas.

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
