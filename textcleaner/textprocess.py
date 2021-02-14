"""Text conversion processing module."""

from typing import List, Dict, Tuple


class InvalidConfig(Exception):
    pass


def process_text(input_text: str, conversion_config: dict) -> str:
    """Processes and converts input text based on config input.

    Args:
        input_text (str): The text to process
        conversion_config (dict): A dict representing conversion steps

    Raises:
        InvalidConfig: Raised if the config is invalid.

    Returns:
        str: The converted text
    """
    valid_config = validate_config(conversion_config)
    if valid_config[0]:
        preprocess = input_text.split("\n")
        if "remove" in conversion_config.keys():
            preprocess = _remove_lines(
                preprocess, tuple(set(conversion_config["remove"]))
            )
        if "replace" in conversion_config.keys():
            preprocess = _replace_text(preprocess, conversion_config["replace"])
        return "\n".join(preprocess)
    else:
        raise InvalidConfig(valid_config[1])


def validate_config(config_data: dict) -> Tuple[bool, str]:
    """Validates a configuration file.

    Args:
        config_data (dict): The configuration to validate.

    Returns:
        Tuple[bool, str]: A tuple containing information representing the pass/fail
                          status of the config. The second element will contain
                          failure information.
    """
    if isinstance(config_data, dict):
        config_keys = config_data.keys()
        if "remove" in config_keys:
            if isinstance(config_data["remove"], list):
                for item in config_data["remove"]:
                    if not isinstance(item, str):
                        return (False, "All items in remove must be of str type")
            else:
                return (False, "'remove' must be a list")
        if "replace" in config_keys:
            if isinstance(config_data["replace"], dict):
                for k, v in config_data["replace"].items():
                    if not isinstance(k, str) or not isinstance(v, str):
                        return (
                            False,
                            f"Invalid remove configuration: '{k}':'{v}'",
                        )
            else:
                return (False, "'replace' must be a dict")
        return (True,)
    else:
        return (False, "Root config is not a dict")


def _remove_lines(input_data: List[str], config_data: Tuple[str, ...]) -> List[str]:
    return [x for x in input_data if not x.startswith(config_data)]


def _replace_text(input_data: List[str], config_data: Dict[str, str]) -> List[str]:
    return [_replace_all(x, config_data) for x in input_data]


def _replace_all(input_str: str, replace_dict: dict) -> str:
    for k, v in replace_dict.items():
        input_str = input_str.replace(k, v)
    return input_str
