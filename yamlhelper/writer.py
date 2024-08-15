import yaml


class BasePrototypeWriter:

    class _CustomDumper(yaml.SafeDumper):
        def represent_ordereddict(self, data):
            return self.represent_dict(data.items())

    def __init__(self, path: str, prototypes: list[dict]):
        self.path = path
        self.prototypes = self._fix_prototypes_structure(prototypes)
        self._CustomDumper.add_representer(dict, self._CustomDumper.represent_ordereddict)

    @staticmethod
    def _filter_none_items(d: dict) -> dict:
        return {k: v for k, v in d.items() if v is not None}

    def _fix_prototypes_structure(self, prototypes: list[dict]) -> list[dict]:
        fixed_prototypes_lst = []
        for prototype in prototypes:
            print(prototype)
            fixed_prototype = {
                "type": prototype.get("type"),
                "id": prototype.get("id"),
                "name": prototype.get("name"),
                "description": prototype.get("description"),
                "parent": prototype.get("parent"),
                "abstract": prototype.get("abstract"),
                "components": prototype.get("components"),
            }

            filtered_fixed_prototype = self._filter_none_items(fixed_prototype)

            fixed_prototypes_lst.append(filtered_fixed_prototype)

        return fixed_prototypes_lst

    def save(self):
        pass


class PrototypeWriter(BasePrototypeWriter):
    def __init__(self, path: str, prototypes: list[dict]):
        super().__init__(path, prototypes)

    def save(self, append: bool = False):
        save_format = "w" if not append else "a"

        yaml_str = ""
        if append:
            yaml_str += "\n"

        try:
            yaml_str += yaml.dump(self.prototypes,
                                  Dumper=self._CustomDumper,
                                  allow_unicode=True,
                                  default_flow_style=False)
        except Exception as e:
            print(e)
        else:
            yaml_str = yaml_str.replace("\n- type", "\n\n- type")

        try:
            with open(self.path, save_format, encoding="utf-8") as file:
                file.write(yaml_str)
        except Exception as e:
            print(e)


class PrototypeChanger(BasePrototypeWriter):
    def __init__(self, path: str,  prototype_id: str, prototype_values: list[dict]):
        super().__init__(path, prototype_values)
        self.prototype_id = prototype_id

    def _find_needed_prototype_index(self, prototypes: list[dict]) -> int:
        for index_, prototype in enumerate(prototypes):
            if prototype.get("id") == self.prototype_id:
                return index_

    def save(self):
        try:
            with open(self.path, encoding="utf-8") as file:
                data: list[dict] = yaml.safe_load(file)
        except Exception as e:
            print(e)

        needed_prototype_index = self._find_needed_prototype_index(data)
        data[needed_prototype_index] = self.prototypes[0]

        yaml_str = ""
        try:
            yaml_str = yaml.dump(data,
                                 Dumper=self._CustomDumper,
                                 allow_unicode=True,
                                 default_flow_style=False)
        except Exception as e:
            print(e)
        else:
            yaml_str = yaml_str.replace("\n- type", "\n\n- type")

        try:
            with open(self.path, "w", encoding="utf-8") as file:
                file.write(yaml_str)
        except Exception as e:
            print(e)
