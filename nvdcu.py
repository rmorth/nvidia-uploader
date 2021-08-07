from moviepy.editor import *
from helpers import input_selection, print_error, input_range, current_time
from config import DEFAULT_CLIP_MODE, DEFAULT_NUM_THREADS, SAVE_CLIPS_TO
from upload import get_authenticated_service, initialize_upload


MAX_THREADS = 4  # FIXME: yeet bad code
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_clip_preferences(clip_name: str, clip_duration: float):
    curtime = current_time()
    clip_name.format(curtime)

    title = input("Insert the title for the clip: ")
    if not title:
        title = 'Default Title'

    description = input("Insert the description for the clip: ")
    if not description:
        description = 'Default description.\n\nUploaded with nvdcu.py :)'

    # get time starting from the end (last 5 seconds)
    error = f"The clip's duration is {clip_duration}s, please insert a valid float.\n"
    time_end = -input_range(message="Time in seconds from the end: ",
                            minimum=0, maximum=clip_duration, integer=False, errors=(None, None, error))

    # get number of threads to be used in the creation of the clip
    error = f"The maximum number of threads allowed is {MAX_THREADS}, please insert a valid integer.\n"
    thread_number = input_range(message="Number of threads used to process clip: ",
                                minimum=1, maximum=MAX_THREADS, default=DEFAULT_NUM_THREADS, errors=(None, None, error))

    # get video's privacy status [(un)listed,(pu)blic,(pr)rivate]
    options = {op[0:2]: op for op in VALID_PRIVACY_STATUSES}
    message = "Select privacy status: "
    privacy_status = options[input_selection(
        options=options, message=message, default='un'
    )]

    pref = {
        'clip_name': f"{SAVE_CLIPS_TO}{clip_name}",
        'title': title,
        'description': description,
        'time_end': time_end,
        'thread_number': thread_number,
        'privacy_status': privacy_status
    }
    print("\nPreferences: ", pref)

    return pref


clip = VideoFileClip("sample.mp4")
new_clip = clip.subclip(t_end=-5)
clip_name = "clip_{}.mp4"  # TODO: change this name

clip_pref = get_clip_preferences(
    clip_name=clip_name, clip_duration=clip.duration)
new_clip.write_videofile(
    clip_name, fps=60, threads=clip_pref['thread_number'])

youtube = get_authenticated_service()
try:
    initialize_upload(youtube=youtube, clip_preferences=clip_pref)
except HttpError as e:
    print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
