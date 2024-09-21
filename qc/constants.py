import os

# Icon path (to be loaded from environment variables)
ICON_PATH = os.getenv('ICON_PATH', 'meulindo.ico')

# Image extensions
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')

# Folder names
SPECIAL_FOLDER = 'Special'
LULZ_FOLDER = 'lulz'
TUT_FOLDER = 'tut'

# File names
RECORD_FILE = 'qc_record.txt'
STATE_FILE = 'qc_state.txt'
MASTER_CSV = 'allQualityControlled.csv'

# Actions
ACTION_DELETE = 'delete'
ACTION_KEEP = 'keep'
ACTION_MOVE = 'move'

# Key bindings
KEY_NEXT = '<Right>'
KEY_PREV = '<Left>'
KEY_DELETE = '<Delete>'
KEY_QUIT = '<Key-q>'
KEY_UNDO = '<BackSpace>'
KEY_SPECIAL = '<Return>'
KEY_LULZ = '<space>'
KEY_TUT = '<Key-t>'