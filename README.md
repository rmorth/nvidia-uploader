# NVIDIA Clip Uploader

Upload clips from NVIDIA GeForce Experience.

## How it works

_TODO_

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

## Resources

- [Moviepy](https://github.com/Zulko/moviepy).
- [YouTube API for videos](https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/youtube_v3.videos.html) and [video upload example](https://developers.google.com/youtube/v3/guides/uploading_a_video).
