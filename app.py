from templating import StreamLitTemplating
from yamlhelper import PrototypeWriter
import streamlit as st


def save_prototype(prototype: list[dict], path, save_method):
    append = False if save_method == "Create new file" else True
    writer = PrototypeWriter(path, prototype)
    writer.save(append=append)


def main():
    temp = StreamLitTemplating("templating/templates/radio_template.json")
    temp.set_values()

    st.header("Saving")
    path = st.text_input("Path to save")
    save_method = st.radio("Choose save method",
                           ["Create new file", "Append to file"], 0)

    if st.button("Save"):
        save_prototype([temp.template], path, save_method)


if __name__ == '__main__':
    main()
