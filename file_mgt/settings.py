"""Settings for Server and Client"""
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8088

TERMINATION_COMMAND = 'quit'
AUTHENTICATION_SUCCESSFUL = 'Authenticaton Succesful'

DATA_DIR = Path(__file__).parent.resolve() / 'data'
USER_DIR = DATA_DIR / 'users'
SESSIONS_FILE = DATA_DIR / 'sessions.csv'
