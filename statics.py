import csv
import sys, os


class NotLogedinError(Exception):
    """Raised token is not valid"""
    pass


base_path = None
try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")

tokens = []

# read tokens
file = open('tokens.csv')
tokenreader = csv.reader(file)
for row in tokenreader:
    tokens.append(row[0])
