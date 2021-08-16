"""Configuration file"""

# Youtube API Related

# Client secrets file location
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Clips
DEFAULT_CLIP_MODE = "from_end"
DEFAULT_NUM_THREADS = 4  # used in processing clip creation
DEFAULT_PRIVACY_STATUS = "unlisted"
DEFAULT_TITLE = "Default Title"
DEFAULT_DESCRIPTION = "No description given.\n\nUploaded with nvdcu.py :)"
DEFAULT_TAGS = "Gaming"  # separated by commas, Tag1,Tag2,...

SAVE_CLIPS_TO = "clips\\"
VIDEO_FOLDER = "samples\\"
ARCHIVE_FOLDER = "archive\\"

COMPRESS_FPS = 30
COMPRESS_RES_HEIGHT = 720
