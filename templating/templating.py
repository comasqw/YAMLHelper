import json
import streamlit as st
from .json_settings import CustomJsonSettings as Json


class _Template:
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


class StreamLitTemplating(_Template):
    def __init__(self, template_path):
        super().__init__(template_path)

    @staticmethod
    def _streamlit_form(type_: str | None = None, **kwargs):
        if type_ is None:
            type_ = Json.STR

        user_input = ""
        if type_ == Json.STR:
            user_input = st.text_input(**kwargs)
        elif type_ == Json.BOOL:
            user_input = st.checkbox(**kwargs)
        elif type_ == Json.INT:
            user_input = int(st.number_input(**kwargs))
        elif type_ == Json.DICT:
            user_input = {}
            kwargs_without_value_and_label = kwargs.copy()
            del kwargs_without_value_and_label["value"]
            del kwargs_without_value_and_label["label"]
            for key, value in kwargs.get("value").items():
                with st.container():
                    key_col, value_col = st.columns(2)
                with key_col:
                    key_input = st.text_input(
                        label="key",
                        value=key,
                        **kwargs_without_value_and_label)
                with value_col:
                    value_input = st.text_input(
                        label="value",
                        value=value,
                        **kwargs_without_value_and_label)
                user_input[key_input] = value_input
            return user_input
        elif type_ == Json.LIST:
            user_input = []
            kwargs_without_value_and_label = kwargs.copy()
            del kwargs_without_value_and_label["value"]
            del kwargs_without_value_and_label["label"]
            for value in kwargs.get("value"):
                element_value = st.text_input(
                    label="",
                    value=value,
                    **kwargs_without_value_and_label
                )
                user_input.append(element_value)
        return user_input

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
                attr_type = value.get(Json.TYPE)
                attr_text = value.get(Json.TEXT)
                if attr_type == Json.BOOL:
                    user_input = self._streamlit_form(attr_type,
                                                      label=key,
                                                      value=default_value)
                else:
                    user_input = self._streamlit_form(attr_type,
                                                      label=key,
                                                      value=default_value,
                                                      placeholder=attr_text,
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
                attr_text = attrs_dct[attr].get(Json.TEXT)
                attr_type = attrs_dct[attr].get(Json.TYPE)
                value = None
                can_be_changed = True
                if attr in default_attrs:
                    attr_values = values.get(Json.ATTRS)[attr]
                    value = attr_values.get(Json.DEFAULT)
                    can_be_changed = attr_values.get(Json.DF_CAN_BE_CHANGED, True)

                if attr_type == Json.LIST:
                    st.subheader(f"{attr} values")

                user_input = self._streamlit_form(
                    attr_type,
                    label=attr_text,
                    value=value,
                    placeholder=attr_text,
                    disabled=not can_be_changed
                )

                result[attr] = user_input
            self.template.get("components").append({"type": component, **result})

    def set_values(self):
        self._set_attributes()
        self._set_components()
