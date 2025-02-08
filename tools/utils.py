from smolagents import tool
from datetime import datetime, timedelta
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

@tool
def stretching_video_link() -> str:
    """To jest narzędzie do zwracania linku do filmu z rozciąganiem."""
    return "https://www.youtube.com/watch?v=VpEqzDHWTB4&ab_channel=BorysMankowskiTazDrill"

@tool
def get_todays_events():
    """Pobiera wszystkie wydarzenia z Kalendarza Google na dzisiaj czyli obecny dzień tygodnia."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    now = datetime.utcnow().isoformat() + "Z"
    end_of_day = (datetime.utcnow().replace(hour=23, minute=59, second=59)).isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary", timeMin=now, timeMax=end_of_day,
        singleEvents=True, orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    return [
        {
            "summary": event.get("summary", "Brak tytułu"),
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
        }
        for event in events
    ]

