import configparser
from os.path import exists


class Configuration():
    def __init__(self):
        self.API_SECTION = 'Youtube API'
        self.CLIP_SECTION = 'Clipping Defaults'
        self.DIR_SECTION = 'Directories'
        self.ARCH_SECTION = 'Archival'
        self.CONFIG_FILE = 'config.ini'

        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE)

        self.config = config
        self.api = config.options(self.API_SECTION)
        self.clipping = config.options(self.CLIP_SECTION)
        self.directories = config.options(self.DIR_SECTION)
        self.archival = config.options(self.ARCH_SECTION)

    def api_client_secrets(self):
        return self.get_option(self.API_SECTION, 'client_secrets_file', path=True)

    def api_upload_scope(self):
        return self.get_option(self.API_SECTION, 'youtube_upload_scope')

    def api_service_name(self):
        return self.get_option(self.API_SECTION, 'youtube_api_service_name')

    def api_version(self):
        return self.get_option(self.API_SECTION, 'youtube_api_version')

    def def_clip_mode(self):
        opt = self.get_option(self.CLIP_SECTION, 'default_clip_mode')
        if not opt in ['e', 'i', 's']:
            raise Exception(
                f'Invalid value ({opt}) for default_clip_mode in section {self.CLIP_SECTION} in {self.CONFIG_FILE}.')
        return opt

    def def_num_threads(self):
        opt = self.get_option(self.CLIP_SECTION, 'default_num_threads')
        try:
            opt = int(opt)
        except:
            raise Exception(
                f'Invalid value ({opt}) for default_clip_mode in section {self.CLIP_SECTION} in {self.CONFIG_FILE}.')
        else:
            return opt

    def def_privacy_status(self):
        opt = self.get_option(self.CLIP_SECTION, 'default_privacy_status')
        if not opt in ['unlisted', 'private', 'public']:
            raise Exception(
                f'Invalid value ({opt}) for default_privacy_status in section {self.CLIP_SECTION} in {self.CONFIG_FILE}.')
        return opt

    def def_title(self):
        return self.get_option(self.CLIP_SECTION, 'default_title')

    def def_description(self):
        return self.get_option(self.CLIP_SECTION, 'default_description')

    def def_tags(self):
        return self.get_option(self.CLIP_SECTION, 'default_tags')

    def dir_clips(self):
        return self.get_option(self.DIR_SECTION, 'clips_folder', path=True)

    def dir_videos(self):
        return self.get_option(self.DIR_SECTION, 'video_folder', path=True)

    def dir_archive(self):
        return self.get_option(self.DIR_SECTION, 'archive_folder', path=True)

    def arch_fps(self):
        opt = self.get_option(self.ARCH_SECTION, 'compress_fps')
        try:
            opt = float(opt)
        except:
            raise Exception(
                f'Invalid value ({opt}) for compress_fps in section {self.ARCH_SECTION} in {self.CONFIG_FILE}.')
        else:
            return opt

    def arch_res_height(self):
        opt = self.get_option(self.ARCH_SECTION, 'compress_res_height')
        try:
            opt = float(opt)
        except:
            raise Exception(
                f'Invalid value ({opt}) for compress_res_height in section {self.ARCH_SECTION} in {self.CONFIG_FILE}.')
        else:
            return opt

    def get_option(self, section: str, option: str, path=False):
        if not self.config.has_option(section, option):
            raise Exception(
                f'Missing {option} in section {section} in {self.CONFIG_FILE}.')

        opt = self.config.get(section, option)
        if path and not exists(opt):
            raise Exception(
                f'Invalid value ({opt}) for {option} in section {section} in {self.CONFIG_FILE}.')

        return opt


CONFIG = Configuration()

CLIENT_SECRETS_FILE = CONFIG.api_client_secrets()
YOUTUBE_UPLOAD_SCOPE = CONFIG.api_upload_scope()
YOUTUBE_API_SERVICE_NAME = CONFIG.api_service_name()
YOUTUBE_API_VERSION = CONFIG.api_version()

DEFAULT_CLIP_MODE = CONFIG.def_clip_mode()
DEFAULT_NUM_THREADS = CONFIG.def_num_threads()
DEFAULT_PRIVACY_STATUS = CONFIG.def_privacy_status()
DEFAULT_TITLE = CONFIG.def_title()
DEFAULT_DESCRIPTION = CONFIG.def_description()
DEFAULT_TAGS = CONFIG.def_tags()

SAVE_CLIPS_TO = CONFIG.dir_clips()
VIDEO_FOLDER = CONFIG.dir_videos()
ARCHIVE_FOLDER = CONFIG.dir_archive()

COMPRESS_FPS = CONFIG.arch_fps()
COMPRESS_RES_HEIGHT = CONFIG.arch_res_height()
