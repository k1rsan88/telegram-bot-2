
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# Подключение к Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds_path = os.path.abspath("credentials.json")
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)
sheet = client.open("Life Tracker").sheet1

# Функция логирования дня
def log_day(sleep_hours, walk, workout, session_start, session_end, notes=""):
    today = datetime.now().strftime("%Y-%m-%d")
    sheet.append_row([today, sleep_hours, walk, workout, session_start, session_end, notes])
