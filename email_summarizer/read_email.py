from __future__ import print_function
import pickle
import os.path

# Google API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Text to speech
import pyttsx3

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
IMPORTANT_LABEL = "CATEGORY_PERSONAL"  # add "UNREAD" in production
LANGUAGE = "fr"


def main():
    """
    1. request emails for gmail account
    2. use text to speach to read email list
    """
    service = gmail_request()
    read_emails(service)


def gmail_request():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)


def read_emails(service):
    results = service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
    messages = results.get("messages", [])
    if not messages:
        print("Vous n'avez pas de nouveaux messages ?")
    else:
        for i, message in enumerate(messages):
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=message["id"], format="raw")
                .execute()
            )
            if "CATEGORY_PERSONAL" in msg["labelIds"]:
                print(msg["snippet"])
                print()
            # say(msg['snippet'])


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    main()