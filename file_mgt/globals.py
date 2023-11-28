"""Global Variables"""
import csv
from pathlib import Path
from settings import SESSIONS_FILE

users = {}
with open(SESSIONS_FILE, encoding='utf-8') as session_file:
    reader = csv.reader(session_file)
    for row in reader:
        [username, password, cwd] = row
        users[username] = {
            'password': password,
            'cwd': Path(cwd),
            'logged_in': False
        }
