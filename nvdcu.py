import argparse
import os
from moviepy.editor import VideoFileClip
from initconfig import DEFAULT_NUM_THREADS, COMPRESS_FPS, COMPRESS_RES_HEIGHT, ARCHIVE_FOLDER
from helpers import input_interval, input_selection, input_range, YoutubeClip, print_info, read_watchlist_file, write_watchlist_file, Watchlist, WatchlistFile, get_videos_in_directory, delete_video, preview_video
from upload import get_authenticated_service

MAX_THREADS = 8  # FIXME: yeet bad code
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_clip_preferences(filepath: str):

    vdf_clip = VideoFileClip(filepath)

    title = input("Insert the title for the clip: ")
    if not title:
        title = 'Default Title'

    description = input("Insert the description for the clip: ")
    if not description:
        description = 'Default description.\n\nUploaded with nvdcu.py :)'

    # get clipping mode [from (e)nd,from (s)tart,(i)nterval]
    options = {"s": "from start, e.g first 10 seconds",
               "e": "from end, e.g last 10 seconds", "i": "time interval"}
    message = "Select clipping mode: "
    mode = input_selection(
        options=options, message=message, default='e')

    # get time starting from the end (last 5 seconds)
    error = f"The clip's duration is {vdf_clip.duration}s, please insert a valid float.\n"
    t = None
    interval = None
    if mode == 'e':
        message = "Time in seconds from the end: "
        t = -input_range(message=message,
                         minimum=0, maximum=vdf_clip.duration, integer=False, errors=(None, None, error))
    elif mode == 's':
        message = "Time in seconds from the start: "
        t = input_range(message=message,
                        minimum=0, maximum=vdf_clip.duration, integer=False, errors=(None, None, error))
    elif mode == 'i':
        message = "Please input an interval (e.g 55 135):"
        interval = input_interval(
            message, minimum=0, maximum=vdf_clip.duration, integer=False)
    else:
        raise Exception(f"Invalid clip mode accepted ({mode})")

    # get number of threads to be used in the creation of the clip
    error = f"The maximum number of threads allowed is {MAX_THREADS}, please insert a valid integer.\n"
    thread_number = input_range(message="Number of threads used to process clip: ",
                                minimum=1, maximum=MAX_THREADS, default=DEFAULT_NUM_THREADS, errors=(None, None, error))

    # get video's privacy status [(un)listed,(pu)blic,(pr)rivate]
    options = {op[0:2]: op for op in VALID_PRIVACY_STATUSES}
    message = "Select privacy status: "
    privacy_status = options[input_selection(
        options=options, message=message, default='un')]

    clip = YoutubeClip(vdf_clip, title=title, description=description, time_from=t, interval=interval, clip_mode=mode,
                       number_of_threads=thread_number, privacy_status=privacy_status, clip_file_name=title+".mp4")
    print(clip)

    return clip


def archive_uploaded(force=False, folder=ARCHIVE_FOLDER):
    print_info("Archiving uploaded files...")
    watchlist = read_watchlist_file()

    for f in watchlist.files:
        if not f.missing:
            if force or f.uploaded and not f.archived:
                archive_video(f, ARCHIVE_FOLDER)

    # Update watchlist file
    write_watchlist_file(watchlist)


def archive_video(f: WatchlistFile, folder=ARCHIVE_FOLDER):
    print_info(f"Archiving video: {f.filepath}")

    vdf = VideoFileClip(f.filepath)
    print("Before:", vdf.filename, vdf.fps, vdf.size)

    if (vdf.size[1] > COMPRESS_RES_HEIGHT):
        vdf = vdf.resize(height=COMPRESS_RES_HEIGHT)

    if (vdf.fps > COMPRESS_FPS):
        vdf = vdf.set_fps(COMPRESS_FPS)

    print("After:", vdf.filename, vdf.fps, vdf.size, "\n")

    vdf.write_videofile(folder + f.filename)
    vdf.close()

    f.archived = True


def checkup(f: WatchlistFile, watchlist: Watchlist, auth_service, ignore_uploaded=False):
    print_info(f"Running checkup for: {f.filename}")

    if not f.uploaded:
        description = """Enter if you wish to:
- Upload: go through the process of uploading this video
- Preview: opens the video in your preferred player
- Delete: permanently delete the video
- Ignore: marks the video as ignored, so it doesn't keep appearing on every script run
- Skip: temporarily skip this video onto the next one

Nothing has been done to this video."""
        message = "Please insert the action you'd like to take: "

        options = {"u": "upload video", "p": "preview video",
                   "d": "delete video", 'i': 'ignore video', 's': 'skip video'}

        confirm = None
        while confirm != 'u':
            confirm = input_selection(
                options, message, default="s", description=description)

            if confirm == 'p':
                preview_video(f)
            elif confirm == 'd':
                delete_video(f, watchlist)
                return
            elif confirm == 'i':
                f.ignored = True
                return
            elif confirm == 's':
                return

        # Clip preferences
        clip = get_clip_preferences(f.filepath)
        clip.write_clip_file()

        # Upload video
        clip.upload(auth_service)
        f.uploaded = True

    if f.uploaded and not ignore_uploaded:
        if f.archived:

            description = """Enter if you wish to:
- Preview: opens the video in your preferred player
- Delete: permanently delete the video
- Ignore: marks the video as ignored, so it doesn't keep appearing on every script run
- Skip: temporarily skip this video onto the next one

This video has been uploaded and archived."""
            options = {"p": "preview video", "d": "delete video",
                       'i': 'ignore video', 's': 'skip video'}

            message = "Please insert the action you'd like to take: "
            confirm = None
            while confirm != 'd':
                confirm = input_selection(
                    options, message, default="s", description=description)

                if confirm == 'p':
                    preview_video(f)
                elif confirm == 'i':
                    f.ignored = True
                    return
                elif confirm == 's':
                    return

            # Delete the video
            delete_video(f)
        else:

            description = """Enter if you wish to:
- Archive: compress video into the ARCHIVE_FOLDER in your config
- Delete: permanently delete the video
- Preview: opens the video in your preferred player
- Ignore: marks the video as ignored, so it doesn't keep appearing on every script run
- Skip: temporarily skip this video onto the next one

This video has been uploaded."""
            options = {"a": "archive video", "d": "delete video", "p": "preview video",
                       'i': 'ignore video', 's': 'skip video'}

            message = "Please insert the action you'd like to take: "

            confirm = None
            while confirm != 'd' and confirm != 'a':
                confirm = input_selection(
                    options, message, default="s", description=description)

                if confirm == 'p':
                    preview_video(f)
                elif confirm == 'i':
                    f.ignored = True
                    return
                elif confirm == 's':
                    return

            if confirm == "a":
                archive_video(f)
            elif confirm == "d":
                delete_video(f, watchlist)


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
    parser.add_argument('--archive-dir', help="overwrite archive directory")
    parser.add_argument('--no-info', action="store_true",
                        help="ommits info messages")
    parser.add_argument('-s', '--status', action="store_true",
                        help="prints watchlist status")
    parser.add_argument('--reset', action="store_true",
                        help="reset watchlist file, see --clean")
    parser.add_argument('--clean', action="store_true",
                        help="clean missing files from watchlist file")

    args = parser.parse_args()

    if args.status:
        print(read_watchlist_file())
        exit()

    if args.archive_dir:
        if not os.path.exists(args.archive_dir):
            print(f"Specified directory is not valid: {args.archive_dir}")
            exit()

        if args.archive_dir[-1] != os.path.sep:
            args.archive_dir = args.archive_dir + os.path.sep
        print_info(f"Overwriting archive directory with: {args.archive_dir}")

        archive_uploaded(directory=args.archive_dir)

    if args.archive_uploaded:
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

    # Youtube API
    auth_service = get_authenticated_service()

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

        if video_to_check.ignored:
            continue
        # Run checkup
        checkup(video_to_check, watchlist, auth_service, args.ignore)

    # Update watchlist
    write_watchlist_file(watchlist)
