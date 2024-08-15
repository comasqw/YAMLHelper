from .parser import YMLParser


class Component:
    def __init__(self, component_name: str, values: dict):
        self.component_name = component_name
        self.values = values

    @property
    def component(self):
        return {self.component_name: self.values}


class Prototype:
    def __init__(self, *,
                 proto_type: str,
                 proto_id: str,
                 components: dict,
                 name: str,
                 description: str,
                 parent: str,
                 abstract: bool,
                 path: str):
        self.proto_type = proto_type
        self.proto_id = proto_id
        self.components = components
        self.name = name
        self.description = description
        self.parent = parent
        self.abstract = abstract
        self.path = path

    @classmethod
    def from_dict(cls, prototype: dict, components: dict, path: str):
        return cls(
            proto_type=prototype.get("type"),
            proto_id=prototype.get("id"),
            name=prototype.get("name"),
            description=prototype.get("description"),
            parent=prototype.get("parent"),
            abstract=prototype.get("abstract"),
            components=components,
            path=path
        )

    @property
    def prototype(self):
        return {
            self.proto_id: {
                "type": self.proto_type,
                "id": self.proto_id,
                "name": self.name,
                "description": self.description,
                "parent": self.parent,
                "abstract": self.abstract,
                "components": [values.component for values in self.components.values()],
                "path": self.path
            }
        }


class Prototypes:
    def __init__(self, prototypes_path: str):
        self._parser = YMLParser(prototypes_path)
        self.prototypes = {}

    async def async_initialize(self):
        prototypes_dct = await self._parser.parse_prototypes()
        for path, prototypes in prototypes_dct.items():
            for prototype, values in prototypes.items():
                components_dct = {}
                components = values.get("components")
                if components:
                    for component in components:
                        components_dct[component.get("type")] = Component(component.get("type"), component)

                self.prototypes[prototype] = Prototype.from_dict(values, components_dct, path)