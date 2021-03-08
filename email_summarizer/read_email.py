from __future__ import print_function
import pickle
import os.path

# Google API
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import base64
from bs4 import BeautifulSoup

# Text to speech
import pyttsx3

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# The kind of email you will collect - more info here -> https://developers.google.com/gmail/api/guides/labels
LABELS = ["INBOX"]  # add "UNREAD" in production
CATEGORIES = ["CATEGORY_PERSONAL"]
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
    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            labelIds=LABELS,
        )
        .execute()
    )
    messages = results.get("messages", [])
    list_of_msg = []
    if not messages:
        print("Vous n'avez pas de nouveaux messages.")
    else:
        for message in messages:
            msg_data = {}
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )
            if (label in msg["labelIds"] for label in CATEGORIES):
                payload = msg["payload"]
                header = payload["headers"]

                for head in header:
                    # Sender
                    if head["name"] == "From":
                        sender = head["value"]
                        sender = [part.strip() for part in sender.split()]
                        name = (" ").join(sender[:-1])
                        msg_data["Sender"] = name
                    # Date
                    if head["name"] == "Date":
                        msg_data["Date"] = head["value"]
                    # Subject
                    if head["name"] == "Subject":
                        msg_data["Subject"] = head["value"]
                print(name)
                # MSG
                mssg_parts = payload["parts"]  # fetching the message parts
                part_one = mssg_parts[0]  # fetching first element of the part
                part_body = part_one["body"]  # fetching body of the message
                part_data = part_body["data"]  # fetching data from the body
                clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
                clean_two = base64.b64decode(
                    bytes(clean_one, "UTF-8")
                )  # decoding from Base64 to UTF-8
                soup = BeautifulSoup(clean_two, "lxml")
                mssg_body = soup.body()
                # mssg_body is a readible form of message body
                # depending on the end user's requirements, it can be further cleaned
                # using regex, beautiful soup, or any other method
                msg_data["Message_body"] = mssg_body
                print(mssg_body)
        print(list_of_msg.append(msg_data))
        # say(msg["snippet"])


def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    main()