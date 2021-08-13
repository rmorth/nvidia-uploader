import argparse
from moviepy.editor import VideoFileClip
from helpers import input_selection, input_range, input_file, YoutubeClip, current_time, print_error, print_info, read_watchlist_file, write_watchlist_file, Watchlist, WatchlistFile, get_videos_in_directory, print_warning, delete_video
from config import DEFAULT_CLIP_MODE, DEFAULT_NUM_THREADS, SAVE_CLIPS_TO, COMPRESS_FPS, COMPRESS_RES_HEIGHT, ARCHIVE_FOLDER
from upload import get_authenticated_service, initialize_upload

MAX_THREADS = 8  # FIXME: yeet bad code
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_clip_preferences(vdf_clip: VideoFileClip, clip_name: str, clip_duration: float):

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
        options=options, message=message, default='un')]

    clip = YoutubeClip(vdf_clip, title=title, description=description, time_from_end=time_end,
                       number_of_threads=thread_number, privacy_status=privacy_status, clip_file_name=clip_name.format(current_time()))
    print(clip)

    return clip


def archive_uploaded(force=False):
    print_info("Archiving uploaded files...")
    watchlist = read_watchlist_file()

    for f in watchlist.files:
        if not f.missing:
            if force or f.uploaded and not f.archived:
                archive_video(f)

    # Update watchlist file
    write_watchlist_file(watchlist)
    print_info("Done.")


def archive_video(f: WatchlistFile):
    print_info(f"Archiving video: {f.filepath}")

    vdf = VideoFileClip(f.filepath)
    print("Before:", vdf.filename, vdf.fps, vdf.size)

    if (vdf.size[1] > COMPRESS_RES_HEIGHT):
        vdf = vdf.resize(height=COMPRESS_RES_HEIGHT)

    if (vdf.fps > COMPRESS_FPS):
        vdf = vdf.set_fps(COMPRESS_FPS)

    print("After:", vdf.filename, vdf.fps, vdf.size, "\n")
    archived_vdf = vdf.write_videofile(ARCHIVE_FOLDER + f.filename)
    vdf.close()

    f.archived = True


def checkup(f: WatchlistFile, watchlist: Watchlist, ignore_uploaded=False):

    print_info(f"Running checkup for: {f.filename}")

    if f.uploaded and not ignore_uploaded:
        if f.archived:
            message = "This video has been uploaded and archived, do you wish to delete the original file? "
            options = {"y": "yes", "n": "no"}
            confirm = input_selection(
                options, message, default="n")

            if confirm == "n":
                return
            # Delete the video
            delete_video(f)
            return
        else:
            description = "- Archiving will compress the video and save it to ARCHIVE_FOLDER in your config.\n- Deleting will permanently delete the original video."
            message = "Do you wish to archive or delete this video? "
            options = {"a": "archive", "d": "delete", "n": "none"}
            confirm = input_selection(
                options, message, default="n", description=description)

            if confirm == "a":
                archive_video(f, watchlist)
            elif confirm == "d":
                delete_video(f, watchlist)

            return

    if not f.uploaded:
        description = "You can upload it later."
        message = "Do you wish to upload this video? "
        options = {"y": "yes", "n": "no"}
        confirm = input_selection(
            options, message, default="n", description=description)

        if confirm == 'n':
            return

        # Clip preferences
        # Upload video


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Manage clips in certain directory.')

    parser.add_argument(
        '-i', '--ignore', '--ignore-uploaded', action="store_true")
    parser.add_argument('-a', '--archive-uploaded',
                        action="store_true", help="archive uploaded videos")
    parser.add_argument('-c', '--config', action="store_true")
    parser.add_argument('--archive-all', action="store_true",
                        help="archive every video")
    parser.add_argument('--no-info', action="store_true",
                        help="ommits info messages")
    parser.add_argument('-s', '--status', action="store_true",
                        help="prints watchlist status")
    parser.add_argument('--reset', action="store_true",
                        help="reset watchlist file, see --clean")
    parser.add_argument('--clean', action="store_true",
                        help="clean missing files from watchlist file")

    args = parser.parse_args()
    print(args)

    if args.status:
        print(read_watchlist_file())
        exit()

    if args.archive:
        description = "This will only archive the ones that haven't been archived.\nIf you wish to force the archival of every uploaded video use --force-archive."
        message = "Are you sure you want to archive already uploaded files? "
        options = {"y": "yes", "n": "no"}
        confirm = input_selection(
            options, message, default="y", description=description)

        if confirm == "n":
            print_info("Cancelling...")
            exit()

        archive_uploaded()
        exit()

    if args.archive_all:
        description = "This will archive EVERY video even if has been archived.\nIf you wish to archive only unarchived videos use --archive -a."
        message = "Are you sure you want to archive all already uploaded files? "
        options = {"y": "yes", "n": "no"}
        confirm = input_selection(
            options, message, default="y", description=description)

        if confirm == "n":
            print_info("Cancelling...")
            exit()

        archive_uploaded(force=True)
        exit()

    if args.config:
        print_info("Configuration mode...")
        exit()

    if args.reset:
        print_info("Resetting watchlist file...")
        write_watchlist_file(Watchlist())
        exit()

    if args.clean:
        print_info("Cleaning watchlist file...")
        watchlist = read_watchlist_file()
        for f in watchlist.files:
            if f.missing:
                watchlist.remove_file(f)
        write_watchlist_file(watchlist)
        exit()

    if args.ignore:
        print_info("Ignoring uploaded files...")
        # NO BREAK

    # Check files in directory VIDEOS_FOLDER:
    videos = get_videos_in_directory()

    # Read files already in watchlist
    watchlist = read_watchlist_file()

    for video in videos:
        video_to_check = None

        for wl_file in watchlist.nonmissing_files():
            if wl_file.filename == video[0]:
                video_to_check = wl_file
                break

        # Not in watchlist
        if not video_to_check:
            # Add to watchlist
            video_to_check = WatchlistFile(video[1])
            watchlist.add_file(video_to_check)

        # Run checkup
        checkup(video_to_check, watchlist, args.ignore)

    # yt_clip = get_clip_preferences(new_clip,clip_name = clip_name, clip_duration = clip.duration)
    # yt_clip.write_clip_file(fps=60)

    # auth_service = get_authenticated_service()
    # yt_clip.upload(auth_service=auth_service)

    # Update watchlist
    write_watchlist_file(watchlist)
