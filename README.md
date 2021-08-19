# NVIDIA Clip Uploader

Upload clips from NVIDIA GeForce Experience.

## Goal

First of all, it's mandatory to state here that this project was made out of enjoyment and curiosity.

With GeForce experience it's easy to create clips with [instant replay](https://www.nvidia.com/en-us/geforce/geforce-experience/shadowplay/). My problem was with uploading them.

GeForce Experience has problems when it comes to keeping you logged in into Google for some reason and it started to bug me. On top of this, the usual process of uploading clips for me was:

1. Make a bunch of instant replays
2. _Time passes..._
3. Filter (delete) through a bunch of unwanted clips
4. Upload the clips you liked

The goal of this script is for it to check the folder in which clips are stored, see which ones haven't been uploaded and prompt you if you wish to upload.

An option for already uploaded clips could be deletion or even archival (compressed).

## Problems

As I went through the hoops with the Youtube API, all of the clips I uploaded through this were flagged as spam and therefore locked as private. In the beginning it didn't happen this often hence it would be a viable script, but unfortunately it happens every single upload now:

<img src="C:\Users\wyllie\AppData\Roaming\Typora\typora-user-images\image-20210819162443115.png" alt="image-20210819162443115" style="zoom: 67%;" />

Apparently Google's API for youtube [restricts unverified applications](https://support.google.com/youtube/answer/7300965), not stating it's without reason I was just unaware of this when I started this. I thought the only limitation was that it'd only work for, manually, whitelisted google accounts (mine) which wouldn't take away any functionality and made this a possible project.

As for the [verification process](https://support.google.com/cloud/answer/9110914?hl=en#zippy=%2Csteps-to-prepare-for-verification), it's just not worth it. So yeah, this is a semi-functioning script in terms of uploading to youtube, the functionality is there but unless you go through the verification process and all that jazz, ain't worth it. This isn't the only problem with the script, but it's the one that severely impacted my motivation to go through with it. You can always archive your videos with it...! 

## How it works

1. Setup your configuration file `config.ini`
   1. Make sure to have your `client_secrets.json` [file ready](https://developers.google.com/youtube/registering_an_application).
   2. Fill in the directories section (with full paths or relative paths).
   3. Optionally, you can change the defaults for the clipping preferences.
2. Run the script and go through your videos in your specified `VIDEO_FOLDER`.
3. You'll be prompted with detailed instructions on how you can proceed with the file in question.

### Flags

You can type `python nvdcu.py -h --help` if you want to see the following text. All flags are optional.

 ```
  -h, --help            				show this help message and exit
  -i, --ignore, --ignore-uploaded	ignores uploaded files while going through watchlist
  -a, --archive-uploaded				archive uploaded videos
  --archive-all         				archive every video
  --archive-dir ARCHIVE_DIR 			overwrite archive directory
  -s, --status          				prints watchlist status
  --reset               				reset watchlist file, see --clean
  --clean               				clean missing files from watchlist file```
 ```


## Requirements

Used **python** (tested with 3.7.3 and 3.9.6).

_Install these requirements via:_ `pip install -r requirements.txt`

- **Moviepy** which uses [ffmpeg](https://ffmpeg.org/)
- **google-api-python-client**
- **httplib2**
- **termtables**
- **colorama**
- **oauth2client**
- **configparser**
- **argparse**

## Resources

- [Moviepy](https://github.com/Zulko/moviepy).
- [YouTube API for videos](https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/youtube_v3.videos.html) and [video upload example](https://developers.google.com/youtube/v3/guides/uploading_a_video).
