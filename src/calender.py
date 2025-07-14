from typing import List
from math import ceil
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path


# Mock lessons for testing purposes
lessons = [
    "Lesson 1",
    "Lesson 2",
    "Lesson 3",
    "Lesson 4",
    "Lesson 5",
   
]

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh()
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


# Goal is to divide the lessons accordingly with date and slot
def get_lesson_day_and_slot(lesson_number: int ) -> List[int]:
    # Determine day
    lesson_day = ceil(lesson_number/3)
    # Determine slot
    lesson_slot = lesson_number % 3
    return [lesson_day,lesson_slot]

def event_handler(event_times: List[int], event_name: str = 'Chess Endgame event'):
    timeslot = {1: '16:00', 2: '16:30', 0: '17:00'}
    day, slot = event_times
    event_date = datetime.today() + timedelta(days=(day - 1))
    event_time = timeslot[slot]
    # Logic for creating event
    # Combine date and time for start and end
    start_datetime = datetime.strptime(f"{event_date.date()} {event_time}", "%Y-%m-%d %H:%M")
    end_datetime = start_datetime + timedelta(minutes=25)

    event = {
        'summary': event_name,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Africa/Johannesburg',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Africa/Johannesburg',
        }
    }

    service = get_calendar_service()
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"✅ Created event: {created_event.get('summary')} at {start_datetime.strftime('%Y-%m-%d %H:%M')}")

""" def add_days_to_today(days: int) -> str:
    future_date = datetime.today() + timedelta(days=days)
    return future_date.strftime("%d/%m/%Y") """
    

# Main function for testing purposes
""" def main():
    for lesson_number,name in enumerate(lessons):
        day_and_slot = get_lesson_day_and_slot(lesson_number+1)
        event_handler(day_and_slot,name)

main() """