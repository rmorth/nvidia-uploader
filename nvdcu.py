from moviepy.editor import *
from helpers import input_selection, print_error, input_range

MAX_THREADS = 4  # FIXME: yeet bad code
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

# TODO: Implement various modes (interval,from_end,from_start,...)


def get_clip_preferences(clip_duration: int):

    # get time starting from the end (last 5 seconds)
    error = f"The clip's duration is {clip_duration}s, please insert a valid float.\n"
    time_end = -input_range(message="Time in seconds from the end: ",
                            minimum=0, maximum=clip_duration, integer=False, errors=(None, None, error))

    # get number of threads to be used in the creation of the clip
    error = f"The maximum number of threads allowed is {MAX_THREADS}, please insert a valid integer.\n"
    thread_number = input_range(message="Number of threads used to process clip: ",
                                minimum=1, maximum=MAX_THREADS, default=4, errors=(None, None, error))

    # get video's privacy status (un,pu,pr)
    options = {op[0:2]: op for op in VALID_PRIVACY_STATUSES}
    message = "Select privacy status: "
    privacy_status = input_selection(
        options=options, message=message, default='un')

    pref = {'time_end': time_end, 'thread_number': thread_number,
            'privacy_status': privacy_status}
    print("\nPreferences: ", pref)

    return pref


clip = VideoFileClip("sample.mp4")
clip_pref = get_clip_preferences(clip_duration=clip.duration)

#new_clip = clip.subclip(t_end=clip_pref['time_end'])

#new_clip.write_videofile("clip.mp4", fps=60, threads=clip_pref['thread_number'])
# https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/youtube_v3.videos.html#insert
# https://developers.google.com/youtube/v3/guides/uploading_a_video
