from typing import List
from math import ceil
from datetime import datetime, timedelta
print('These are all the lessons available: ')

lessons = [
    "Lesson 1",
    "Lesson 2",
    "Lesson 3",
    "Lesson 4",
    "Lesson 5",
    "Lesson 6",
    "Lesson 7",
    "Lesson 8",
    "Lesson 9",
    "Lesson 10",
    "Lesson 11"
]

# Goal is to divide the lessons accordingly with date and slot
def get_lesson_day_and_slot(lesson_number: int ) -> List[int]:
    # Determine day
    lesson_day = ceil(lesson_number/3)
    # Determine slot
    lesson_slot = lesson_number % 3
    return [lesson_day,lesson_slot]

def event_handler(event_times: List[int]):
    timeslot = {1: '4:00 PM', 2: '4:30 PM', 0: '5:00 PM'}
    day, slot = event_times
    event_date = add_days_to_today(day-1)
    print(f'Date: {event_date}',end=' ')
    print(f'Time: {timeslot[slot]}')

def add_days_to_today(days: int) -> str:
    future_date = datetime.today() + timedelta(days=days)
    return future_date.strftime("%d/%m/%Y")
    

def main():
    for lesson_number,name in enumerate(lessons):
        day_and_slot = get_lesson_day_and_slot(lesson_number+1)
        print(name, end=' ')
        event_handler(day_and_slot)

main()