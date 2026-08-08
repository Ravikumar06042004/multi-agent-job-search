import sqlite3
import os
import imaplib
import email
from email.header import decode_header

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "jobs.db")

EMAIL = "b.y.ravi987@gmail.com"
APP_PASSWORD = "ddiy sbhq olpk xifo"


def get_connection():
    return sqlite3.connect(DB_PATH)


def update_interview_status(company):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE applications
        SET status='Interview'
        WHERE company LIKE ?
        """,
        (f"%{company}%",)
    )

    conn.commit()
    conn.close()


def monitor_inbox():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, "(UNSEEN)")

    if status != "OK":
        print("Could not read inbox.")
        return

    email_ids = messages[0].split()

    # Check only the last 10 unread emails
    email_ids = email_ids[-10:]

    interview_keywords = [
        "interview",
        "technical interview",
        "interview invitation",
        "schedule interview",
        "technical round",
        "coding round",
        "assessment",
        "screening",
        "round 1",
        "round 2"
    ]

    detected_companies = set()

    for eid in email_ids:
        status, msg_data = mail.fetch(eid, "(RFC822)")

        if status != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1])

        subject = msg.get("Subject", "")
        decoded = decode_header(subject)[0]

        if isinstance(decoded[0], bytes):
            subject = decoded[0].decode(decoded[1] or "utf-8")

        sender = msg.get("From", "")

        text = (subject + " " + sender).lower()

        if any(keyword in text for keyword in interview_keywords):
            company = sender.split("@")[-1].split(".")[0]

            if company not in detected_companies:
                update_interview_status(company)
                detected_companies.add(company)
                print(f"Interview detected from {company}")

    if not detected_companies:
        print("No new interview emails found.")

    mail.logout()


if __name__ == "__main__":
    monitor_inbox()