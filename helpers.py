"""Helper functions that can be used throughout the program."""
from colorama import Fore, Back, Style
import termtables as tt
from moviepy.editor import *
from datetime import datetime


def input_selection(options: dict, message="Select from these options: ", default=None, error_message="Please insert from the available options."):
    """input from a selection of options

    Parameters
    ----------
    options : dict
        options accepted in input, e.g: {"u": "unlisted"}
    message : str, optional
        message to show in input, by default "Select from these options {}: "
    default : str, optional
        default value to use if input is empty, by default is None
    error_message : str, optional
        if input isn't in options, by default "Please insert from the available options."

    Returns
    -------
    str
        returns input from user as string
    """

    if len(options) < 2:
        raise Exception(
            f"Options parameter is invalid (length={len(options)}).")

    header = ["Option Description", "Option Value"]
    data = [[opt, key] for key, opt in options.items()]
    tt.print(data, header=header)

    if default != None:
        message = f"[default={default}] " + message

    invalid_input = True
    while invalid_input:
        value = input(message)

        if default != None and value == '':
            return default

        invalid_input = value not in options.keys()
        if invalid_input:
            print_error(f"{error_message}\n")
    return value


# TODO: syntax for errors is a bit wonky
def input_range(message="Please insert a value: ", default=None, minimum=None, maximum=None, integer=True, errors=(None, None, None)):
    """input within a range (inclusive limits)

    Parameters
    ----------
    message : str, optional
        message to show in input, by default "Please insert a value: "
    default : int | float, optional
        default value if user doesn't input anything, by default None
    minimum : int | float, optional
        minimum value for input, by default None
    maximum : int | float, optional
        maximum value for input, by default None
    integer : bool, optional
        if input is integer (or float), by default True
    errors : tuple, optional
        ("input isn't integer", "input is below minimum", "input is above maximum"), by default (None,None,None)

    Returns
    -------
    int | float
        return is determined by integer parameter
    """

    if len(errors) != 3:
        raise Exception(f"Errors parameter is invalid (length={len(errors)}).")

    if integer:
        input_type = "integer"
    else:
        input_type = "float"

    message = f"[{minimum},{maximum}] " + message
    if default != None:
        message = f"[default={default}] " + message

    invalid_input = True
    while invalid_input:
        try:
            value = input(message)
            if default != None and value == '':
                return default
            if integer:
                value = int(value)
            else:
                value = float(value)
        except:
            if errors[0] == None:
                print_error(f"Please insert an {input_type}.\n")
            else:
                print_error(errors[0])

        else:
            if minimum != None and value < minimum:
                if errors[1] == None:
                    print_error(
                        f"Please insert a {input_type} greater or equal to {minimum}.\n")
                else:
                    print_error(errors[1])

            elif maximum != None and value > maximum:
                if errors[2] == None:
                    print_error(
                        f"The maximum value is {maximum}, please insert a valid {input_type}.\n")
                else:
                    print_error(errors[2])
            else:
                invalid_time = False
                break
    return value


def print_error(message: str):
    msg = f"{Fore.WHITE + Back.RED}[ERROR]{Style.RESET_ALL} {message}"
    print(msg)


def current_time():
    return round(datetime.utcnow().timestamp() * 1000)
