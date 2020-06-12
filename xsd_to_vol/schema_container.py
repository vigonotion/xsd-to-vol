class SchemaContainer:
    def __init__(self, name, schema, documentation, requirements):
        self.name = name
        self.schema = schema
        self.documentation = documentation
        self.requirements = requirements

    def __str__(self):
        return f'"""{self.name}\n\n{self.documentation}\n"""\n\n{self.name} = {self.schema}'
