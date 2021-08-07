"""Configuration file"""
# Client secrets file location
CLIENT_SECRETS_FILE = "client_secrets.json"

# Youtube API Relateda

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Clips
DEFAULT_CLIP_MODE = "from_end"
DEFAULT_NUM_THREADS = 4  # used in processing clip creation
SAVE_CLIPS_TO = "clips/"
