"""
Tachistostory - Configuration Settings
Contains all application constants and configuration values.
"""

import os

# Application version
APP_VERSION = '0.9.0'

# Center the window on screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Slider duration constants (in milliseconds)
DURATA_MIN = 220  # Minimum word display duration
DURATA_MAX = 1200  # Maximum word display duration

# Minimum window dimensions
MIN_WIDTH = 600
MIN_HEIGHT = 400

# Slider position constants (can be calculated dynamically)
X_MIN = 100
X_MAX = 500
<<<<<<< HEAD

INTRO_TABLE_DURATION = 2000
=======
>>>>>>> 1982162 (Initial commit)
