import json
import os
import PySimpleGUI as sg
import pyperclip

from textcleaner.textprocess import InvalidConfig, process_text, validate_config


def app():
    sg.theme("DarkAmber")  # Add a touch of color
    # All the stuff inside your window.
    settings = sg.UserSettings()
    config_data = None
    layout = [
        [sg.Text("Load Configuration:")],
        [
            sg.Input(settings.get("-filename-"), key="-IN-"),
            sg.FileBrowse(file_types=(("TextCleanerConfig", "*.tcConfig"),)),
        ],
        [sg.Button("Load", key="-load-")],
        [sg.Text("Not Loaded", key="-load_status-", size=(20, 1), text_color="red")],
        [sg.Text("_" * 60)],
        [sg.Text("Input:")],
        [sg.Multiline("", key="-INPUT-", size=(60, 15))],
        [sg.Button("Process", key="-process-", disabled=True)],
        [sg.Text("Output:")],
        [sg.Multiline("", key="-OUTPUT-", size=(60, 15), disabled=True)],
        [sg.Button("Copy", key="-copy-", disabled=True)],
        [sg.Text("_" * 60)],
        [sg.Button("Close")],
    ]

    # Create the Window
    window = sg.Window("Text Cleaner", layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Close":
            break
        elif event == "-load-":
            pre_file = values["-IN-"]
            if not pre_file.endswith(".tcConfig"):
                sg.PopupError("Invalid file type")
            elif not os.path.isfile(pre_file):
                sg.PopupError("File cannot be found")
            else:
                config_data = None
                settings["-filename-"] = ""
                window["-process-"](disabled=True)
                window["-copy-"](disabled=True)
                window["-OUTPUT-"].update("")
                with open(pre_file, "r") as op_file:
                    config_raw = op_file.read()
                try:
                    config_data = json.loads(config_raw)
                    valid_config = validate_config(config_data)
                    if not valid_config[0]:
                        sg.PopupError(valid_config[1])
                        config_data = None
                except ValueError:
                    sg.PopupError("Invalid file content")
                if config_data:
                    settings["-filename-"] = pre_file
                    window["-load_status-"](
                        f"{settings['-filename-'].split('/')[-1]} Loaded",
                        text_color="green",
                    )
                    window["-process-"](disabled=False)
        elif event == "-process-":
            try:
                window["-OUTPUT-"].update(process_text(values["-INPUT-"], config_data))
                window["-copy-"](disabled=False)
                pyperclip.copy(values["-OUTPUT-"])
            except InvalidConfig as e:
                sg.PopupError(e)
        elif event == "-copy-":
            pyperclip.copy(values["-OUTPUT-"])

    window.close()


if __name__ == "__main__":
    app()
