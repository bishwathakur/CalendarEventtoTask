import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/tasks",
]


def events_to_json(events):
    event_list = []
    for event in events:
        event_dict = {
            "summary": event["summary"],
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
        }
        event_list.append(event_dict)
    return event_list

def get_credentials():
    """Gets valid user credentials from local storage."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def create_task(service, task_list_id, title):
    """Create a task in Google Tasks."""
    task = {"title": title}
    service.tasks().insert(tasklist=task_list_id, body=task).execute()

def main():
    creds = get_credentials()
    service_calendar = build("calendar", "v3", credentials=creds)
    service_tasks = build("tasks", "v1", credentials=creds)

    # Get today's date
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min).isoformat() + "Z"
    end_of_day = datetime.datetime.combine(today, datetime.time.max).isoformat() + "Z"

    try:
        # Call the Calendar API
        events_result = (
            service_calendar.events()
            .list(
                calendarId="primary",
                timeMin=start_of_day,
                timeMax=end_of_day,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No events found for today.")
            return

        # Convert events to JSON
        json_events = events_to_json(events)

        # Save events in JSON format
        filename = f"jsons/eventsOf_{today}.json"
        with open(filename, "w") as json_file:
            json.dump(json_events, json_file, indent=4)

        print(f"Today's events saved in '{filename}'.")

        # Create tasks for each event
        task_list_id = "@default"  # Default task list
        for event in events:
            event_title = event["summary"]
            create_task(service_tasks, task_list_id, event_title)
            print(f"Task created: {event_title}")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
