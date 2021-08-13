"""Helper functions that can be used throughout the program."""
from colorama import Fore, Back, Style
import termtables as tt
from moviepy.editor import *
from datetime import datetime
from config import DEFAULT_CLIP_MODE, DEFAULT_NUM_THREADS, DEFAULT_PRIVACY_STATUS, DEFAULT_DESCRIPTION, DEFAULT_TITLE, SAVE_CLIPS_TO, VIDEO_FOLDER
from upload import initialize_upload
from apiclient.errors import HttpError


class YoutubeClip():
    def __init__(self, clip=VideoFileClip, title=DEFAULT_TITLE, description=DEFAULT_DESCRIPTION, time_from_end=None, number_of_threads=DEFAULT_NUM_THREADS, privacy_status=DEFAULT_PRIVACY_STATUS, clip_file_name=None, clip_mode=DEFAULT_CLIP_MODE):
        self.title = title
        self.description = description
        self.time_from_end = time_from_end
        self.number_of_threads = number_of_threads
        self.privacy_status = privacy_status
        self.clip = clip

        if clip_file_name:
            self.clip_file_name = clip_file_name
        else:
            self.clip_file_name = current_time()

        self.clip_file_name = f"{SAVE_CLIPS_TO}{self.clip_file_name}"

        self.clip_mode = clip_mode

        if self.clip_mode == "from_end" and self.time_from_end == None:
            # FIXME: better exception
            raise Exception("Invalid youtube clip instance.")

    def write_clip_file(self, fps=60):
        self.clip.write_videofile(self.clip_file_name, fps=fps,
                                  threads=self.number_of_threads)

    def upload(self, auth_service):
        try:
            initialize_upload(youtube=auth_service, clip=self)
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

    def __str__(self):
        header = ["Preference", "Value"]
        data = [
            ["Title", self.title],
            ["Description", self.description.encode(
                'unicode-escape').decode()],
            ["Time from end", self.time_from_end],
            ["Privacy Status", self.privacy_status],
            ["Num. Threads", self.number_of_threads],
            ["File Name", self.clip_file_name],
            ["Clip Mode", self.clip_mode]
        ]

        return tt.to_string(data, header=header)


class WatchlistFile():
    def __init__(self, filepath, archived=False, uploaded=False, missing=False):
        self.filepath = filepath
        self.relpath = os.path.relpath(filepath)
        self.filename = os.path.basename(filepath)
        self.archived = archived
        self.uploaded = uploaded
        self.missing = missing

    def __str__(self):
        data = [
            ["Filepath", self.filepath],
            ["Relpath", self.relpath],
            ["Filename", self.filename],
            ["Archived?", self.archived],
            ["Uploaded?", self.uploaded]
        ]
        return tt.to_string(data)


class Watchlist():
    def __init__(self, files=None):
        self.archived_count = 0
        self.uploaded_count = 0
        self.files = []
        if files:
            for f in files:
                assert type(f) == WatchlistFile
                self.add_file(f)

    def nonmissing_files(self):
        return filter(lambda f: f.missing == False, self.files)

    def add_file(self, f: WatchlistFile):
        self.files.append(f)
        self.update_counters(f)

    def remove_file(self, f: WatchlistFile):
        print(f"Index of file: {self.files.index(f)}")
        pass

    def update_counters(self, f: WatchlistFile):
        if f.archived:
            self.archived_count += 1
        if f.uploaded:
            self.uploaded_count += 1

    def __str__(self):
        if len(files) == 0:
            return ""

        header = ["Filepath", "Archived", "Uploaded"]
        data = []
        for f in self.files:
            data.append([f.filepath, f.archived, f.uploaded])

        stats = f"\nTotal: {len(files)} Archived: {self.archived_count} Uploaded: {self.uploaded_count}"
        return tt.to_string(data, header=header) + stats

    def __sizeof__(self):
        return len(self.files)

    def __len__(self):
        return len(self.files)


def input_selection(options: dict, message="Select from these options: ", description=None, default=None, error_message="Please insert from the available options."):
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

    if description:
        print(description + "\n")

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
    # TODO: syntax for errors is a bit wonky
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


def input_file(message: str, directory=VIDEO_FOLDER):
    invalid_input = True
    while invalid_input:
        fname = input(
            f"[IN: '{directory}'] Enter the filename that you wish to clip: ")
        if not fname:
            print("Please insert a valid filename.")
            # TODO: Print valid files in directory?
        else:
            if not os.path.exists(f"{directory}{fname}"):
                print("The file you entered does not exist.")
            else:
                invalid_input = False


def print_error(message: str):
    msg = f"{Fore.WHITE + Back.RED}[ERROR]{Style.RESET_ALL} {message}"
    print(msg)


def print_info(message: str):
    msg = f"{Fore.BLACK + Back.LIGHTWHITE_EX}[INFO]{Style.RESET_ALL} {message}"
    print(msg)


def print_warning(message: str):
    msg = f"{Fore.WHITE + Back.YELLOW}[WARN]{Style.RESET_ALL} {message}"
    print(msg)


def current_time():
    return round(datetime.utcnow().timestamp() * 1000)


def read_watchlist_file():
    print_info("Reading watchlist file...")

    # We're dealing with filepaths, need exaggerated separators
    fname = "watchlist.txt"
    arg_separator = " ---------- "  # - x 10

    files = Watchlist()
    invalid_files = 0

    with open(fname, "r") as data_file:
        lines = list(filter(lambda line: len(line) > 0, data_file.readlines()))

        for line in lines:
            f, archived, uploaded = line.split(sep=arg_separator)

            missing = False
            if not os.path.exists(f):
                print_warning(f"Couldn't find file: {f}")
                invalid_files += 1
                missing = True

            try:
                archived = bool(int(archived))
                uploaded = bool(int(uploaded))
            except Exception as e:
                print_error(
                    f"Error parsing watchlist file arguments! [f={f},a={archived},u={u}]")
                raise

            files.add_file(WatchlistFile(f, archived, uploaded, missing))

        data_file.seek(0)

    print_info(
        f"Successfully parsed watchlist file! {len(files)} files parsed. {invalid_files} files missing.")

    return files


def write_watchlist_file(watchlist: Watchlist):
    print_info("Writing watchlist file...")

    arg_separator = " ---------- "  # - x 10

    with open("watchlist.txt", "w+") as watchfile:
        for f in watchlist.files:
            line = f"{f.filepath}{arg_separator}{int(f.archived)}{arg_separator}{int(f.uploaded)}\n"
            watchfile.write(line)

    print_info("Done.")


def get_videos_in_directory():
    videos = []
    for folder, sub_folders, dir_files in os.walk(VIDEO_FOLDER):
        for f in dir_files:
            if f[-4:] == '.mp4':
                videos.append((f, os.path.realpath(f)))
    return videos


def delete_video(f: WatchlistFile, watchlist: Watchlist):
    print_info(f"Deleting video: {f.filepath}")
    try:
        os.remove(f.filepath)
        watchlist.remove_file(f)
    except Exception as e:
        print_error("There was a problem deleting the video!")
        print_error(e.message)
    else:
        print_info("Successfully deleted the video.")


if __name__ == "__main__":  # DEBUG
    files = read_watchlist_file()
    # os.system(f'totem "{files.files[0].filepath}"')
    write_watchlist_file(files)
