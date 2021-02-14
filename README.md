# TextCleaner Readme
Version: `0.1.0`

TextCleaner is a simple Python app that takes an input text string and alters it by removing and replacing content based on a configuration file. 

## Installation
 1. Clone the repository to your computer
 2. Navigate to the cloned folder with your command prompt/shell of choice
 3. Create and activate a virtual environment if you wish ([venv](https://docs.python.org/3/library/venv.html))
 4. Run `python -m pip install -r requirements.txt`
 5. Run `python -m textcleaner` to start the app

## Development
This app was built with [Poetry](https://python-poetry.org/). I recommend installing Poetry if you wish to work with the deployment features and the `pyproject.toml` file

## Config File Format
 * Config files are JSON files with the file extension: `*.tcConfig`.
 * There are two sections in the current format: `remove` and `replace`
 * Strings in the `remove` list will cause any line of text that starts with that string to be removed from the output 
 * Key value pairs in the `replace` dict define what to replace (attribute) and what to replace them with (value)
 * List item

The files should be formatted similarly to this:
```JSON
{
  "remove": [
    "Line 1",
    "Line 2"
  ],
  "replace": {
    "IncorrectIncorrect": "Incorrect",
    "CorrectCorrect": "Correct"
  }
}
```