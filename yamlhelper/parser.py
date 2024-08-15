import yaml
import os
import aiofiles


class YMLParser:
    def __init__(self, prototypes_path: str):
        self.prototypes_path = prototypes_path

    def _get_files_paths(self) -> list:
        files_paths_lst = []
        try:
            for dirpath, _, filenames in os.walk(self.prototypes_path):
                for filename in filenames:

                    if not filename.endswith(".yml"):
                        continue

                    path = f"{dirpath}\\{filename}"
                    files_paths_lst.append(path)
        except Exception as e:
            print(e)

        return files_paths_lst

    @staticmethod
    async def _read_file(path: str) -> list[dict]:
        try:
            async with aiofiles.open(path, encoding="utf-8") as file:
                content = await file.read()
                data = yaml.safe_load(content)
        except Exception as e:
            print(e)
        else:
            return data

    async def parse_prototypes(self) -> dict:
        all_prototypes = {}
        for path in self._get_files_paths():

            all_prototypes[path] = {}

            data: list[dict] = await self._read_file(path)

            if data is not None:
                for prototype in data:
                    all_prototypes[path][prototype.get("id")] = prototype

        return all_prototypes
