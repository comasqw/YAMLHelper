import json
import streamlit as st
from .json_settings import CustomJsonSettings as Json


class Template:
    def __init__(self, template_path):
        self.template, self.info_template = self._read_template(template_path)
        self.components = self._read_components()

    @staticmethod
    def _read_components():
        try:
            with open("templating/templates/components.json", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            print(e)
            return {}

    @staticmethod
    def _read_template(template_path: str):
        try:
            with open(template_path, encoding="utf-8") as file:
                template_data = json.load(file)
        except Exception as e:
            print(e)

        template = {}
        for key, value in template_data.items():
            if key == Json.TEMPLATE_NAME:
                continue
            if key == "type":
                template[key] = value
                continue

            if key != "components":
                template[key] = "" if not value.get(Json.DEFAULT) else value.get(Json.DEFAULT)
            else:
                template[key] = []

        return template, template_data


class StreamLitTemplating(Template):
    def __init__(self, template_path):
        super().__init__(template_path)

    def _set_attributes(self):
        for key, value in self.info_template.items():
            if key == Json.TEMPLATE_NAME:
                st.title(value)
                st.header("attributes")
            elif key in ("type", "components"):
                continue
            else:
                default_value = value.get(Json.DEFAULT)
                can_be_changed = value.get(Json.DF_CAN_BE_CHANGED, True)
                if value.get("type") == "bool":
                    user_input = st.checkbox(label=key, value=default_value)
                else:
                    user_input = st.text_input(label=key,
                                               value=default_value,
                                               placeholder=value.get("text"),
                                               disabled=not can_be_changed)

                self.template[key] = user_input

    def _set_components(self):
        components = self.info_template.get("components")
        st.header("components")
        for component, values in components.items():
            component_text = self.components.get(component).get(Json.TEXT)
            st.subheader(f"{component} - {component_text}")
            attrs_dct = self.components.get(component).get(Json.ATTRS)
            attrs_lst = [key for key in attrs_dct]
            default_attrs = [key for key in values.get(Json.ATTRS, [])]
            multiselect_disabled = values.get(Json.CAN_BE_ADDED_ATTRIBUTES, True)

            options = st.multiselect(
                label="Component attributes",
                options=attrs_lst,
                default=default_attrs,
                disabled=not multiselect_disabled
            )

            result = {}
            for attr in options:
                value = None
                can_be_changed = False
                if attr in default_attrs:
                    attr_values = values.get(Json.ATTRS)[attr]
                    value = attr_values.get(Json.DEFAULT)
                    can_be_changed = attr_values.get(Json.DF_CAN_BE_CHANGED, False)

                user_input = st.text_input(
                    label=attrs_dct[attr],
                    value=value,
                    placeholder=attrs_dct[attr],
                    disabled=can_be_changed
                )

                result[attr] = user_input
            self.template.get("components").append({"type": component, **result})

    def set_values(self):
        self._set_attributes()
        self._set_components()


class ConsoleTemplating(Template):
    def __init__(self, template_path: str):
        super().__init__(template_path)

    def _set_attributes(self):
        for key, value in self.info_template.items():
            if key == "template_name":
                print(f"Название Шаблона - {value}")
            elif key == "type":
                print(f"{key} - {value}")
            elif key == "components":
                continue
            else:
                default_value = value.get("default")
                print(f"{key} = {default_value}")
                if value.get("default_can_be_changed") is False:
                    continue

                user_input = input(f'{value.get("text")}: ')
                if user_input == "_default_":
                    continue

                if value.get("type") == "bool":
                    self.template[key] = user_input == "True"
                else:
                    self.template[key] = user_input

    def set_components(self):
        pass

    def set_values(self):
        self._set_attributes()
        print(self.template)


if __name__ == '__main__':
    temp = ConsoleTemplating("templates/test.json")
    temp.set_values()
