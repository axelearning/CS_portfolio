import imaplib
import email
import re
import os
import pyttsx3


EMAIL_ADRESS = os.environ.get("EMAIL_USER")
PWD = os.environ.get("EMAIL_PWD")
SMTP_SERVER = "smtp.gmail.com"


class emailReader:
    """
    1. Get Email using SMTP protocol via IMAP
    2. Format the emails
    3. Text to speach
    """

    def __init__(self, email_adress=EMAIL_ADRESS, host=SMTP_SERVER):
        self.emails = []
        self.get_email_client(email_adress)
        self.get_emails()
        self.speak()

    def get_email_client(self, email_adress, password=PWD):
        """
        Initialize IMAP & Login
        ---
            RETURN: [NONE]
        ---
        email_adress: email_adress you want to use
        password_file: file where you store your password
        """
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        try:
            mail.login(email_adress, password)
        except:
            print("LOGIN FAILED")
        self.mail = mail

    def get_uids(self, folder="INBOX", category="Primary", unseen=True):
        """
        Get email uid (unique id)
        ---
        RETURN: List of msg ids
        ---
        folder : to access a specific folder: - (INBOX,[Gmail]/Spam)
        category : search email from a particular category - (Primary, Promotional, Updates, Forums)
        unseen : True - only unseen msg
        """
        # Acess a specific folder
        self.mail.select(folder, readonly=True)

        # Filter by category
        _, response = self.mail.uid("search", 'X-GM-RAW "category:' + category + '"')
        filtred_msg_ids = response[0].decode("utf-8").split()

        # Grab only unseen msg ?
        if unseen:
            _, response = self.mail.uid("search", None, "UNSEEN")
            unseen_msg_ids = response[0].decode("utf-8").split()
            return [msg for msg in filtred_msg_ids if msg in unseen_msg_ids]
        else:
            return filtred_msg_ids

    def get_emails(self, **kwargs):
        """
        Get Emails from ids in a raw formats
        """
        for uid in self.get_uids(**kwargs):
            email_msg = {}
            _, data = self.mail.uid("fetch", uid, "(RFC822)")
            msg = self.get_msg_object(data)
            # headers
            for header in ["From", "Subject", "Date"]:
                email_msg[header] = msg[header]
            # body
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_msg["body"] = self.format(body)
                if part.get_content_type() == "text/html":
                    body = part.get_payload(decode=True)
                    email_msg["html"] = self.format(body)
            self.emails.append(email_msg)

    @staticmethod
    def get_msg_object(data):
        for part in data:
            if isinstance(part, tuple):
                return email.message_from_bytes(part[1])

    @staticmethod
    def format(body):
        """
        Format my email into a good format
        """
        body = body.decode()
        # remove links
        regex = re.compile(r"(\[.*?\](\r\n)?)?<https://.*?>")
        body = re.sub(regex, "", body)
        return body

    def speak(self):
        engine = pyttsx3.init()
        engine.say(f"Vous avez {len(self.emails)} nouveau messages")
        engine.runAndWait()
        for n, email in enumerate(self.emails):
            name = self.get_recipient_name(email["From"])
            print(name)
            print(email["Subject"])
            print(email["body"])
            print("---")
            engine.say(f"Le Message numéro {n+1} vient de: {name}")
            engine.say(email["Subject"])
            engine.say(email["body"])
            engine.runAndWait()

    @staticmethod
    def get_recipient_name(email):
        return email.split("<")[0]


if __name__ == "__main__":
    m = emailReader()