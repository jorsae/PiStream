import re

STATIC_FOLDER = ''

DATABASE_FILE = '../PiStream.sql'


MAX_VIDEO_RESULTS = 30

WATCH_PROGRESS_TIME_EDGE = 90

VIDEO_FORMATS = ['.mp4', '.m4v']
SUBTITLE_FORMATS = ['.vtt']


RE_SUBTITLE_EXTENSION = re.compile("^\.\w{2}$")