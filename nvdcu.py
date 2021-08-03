from moviepy.editor import *
from colorama import Fore, Back, Style

MAX_THREADS = 4  # FIXME: yeet bad code

# TODO: Implement various modes (interval,from_end,from_start,...)
# TODO: separate inputs/errors into different module
# TODO: Generalise inputs (type,min,max,etc.)


def get_clip_preferences(clip_duration: int):
    time_end = get_clip_time(clip_duration=clip_duration)
    thread_number = get_clip_nrthreads()
    options = {'u': 'unlisted', 'pr': 'private', 'pu': 'public'}
    video_access = input_from_selection(
        options=options, message="Select video access {}:")

    pref = {'time_end': -time_end, 'thread_number': thread_number,
            'video_access': video_access}
    print("\nPreferences: ", pref)
    return pref


def get_clip_time(clip_duration):
    invalid_time = True
    while invalid_time:
        try:
            time_end = int(
                input(f"[max={clip_duration}s] Time in seconds from the end (*): "))
        except:
            print_error("Please insert an integer.\n")
        else:
            if time_end < 0:
                print_error(
                    "Please insert an integer greater or equal to 0.\n")
            elif time_end > clip_duration:
                print_error(
                    f"The clip's duration is {clip_duration}s, please insert a valid integer.\n")
            else:
                invalid_time = False
                break
    return time_end


def get_clip_nrthreads():
    invalid_thread_number = True
    while invalid_thread_number:
        try:
            thread_number = input(
                f"[max={MAX_THREADS}] Number of threads (enter for default=4): ")

            if thread_number == '':
                thread_number = 4
            else:
                thread_number = int(thread_number)
        except:
            print_error("Please insert an integer.\n")
        else:
            if thread_number < 0:
                print_error(
                    "Please insert an integer greater or equal to 0.\n")
            elif thread_number > MAX_THREADS:
                print_error(
                    f"The maximum number of threads allowed is {MAX_THREADS}, please insert a valid integer.\n")
            else:
                invalid_thread_number = False
                break
    return thread_number


def input_from_selection(options: dict, message="Select from these options {}: ", error_message="Please insert from the available options."):
    invalid_input = True
    while invalid_input:
        value = input(message.format(options))
        invalid_input = value not in options.keys()
        if invalid_input:
            print_error(f"{error_message}\n")
    return value


def print_error(message: str):
    msg = f"{Fore.WHITE + Back.RED}[ERROR]{Style.RESET_ALL} {message}"
    print(msg)


clip = VideoFileClip("sample.mp4")
clip_pref = get_clip_preferences(clip_duration=clip.duration)

#new_clip = clip.subclip(t_end=clip_pref['time_end'])

#new_clip.write_videofile("clip.mp4", fps=60, threads=clip_pref['thread_number'])
# TODO: Look into google API for video uploading
