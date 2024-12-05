
import asyncio

import imaplib
import email
from email.header import decode_header
import configure
import httpx

async def notifyme_announce(message):
    """ Announce messages using Echo Dot Devices and the Notify-Me Skill """
    print(f"announce: '{message}'")
    async with httpx.AsyncClient() as client:
        url = "https://api.notifymyecho.com/v1/NotifyMe"
        response = await client.post(url,
                json = {
                'accessCode': configure.NOTIFICATIONS_TOKEN,
                'notification': message
                }) 
        print(f"NotifyMe Response: {response.text}")


async def voice_monkey(message="INSERT YOUR MESSAGE HERE", device=configure.VOICEMONKEY_DEVICE):
    print(f"Initiating Voice Monkey message to device {device}")
    async with httpx.AsyncClient() as client:
        url = "https://api-v2.voicemonkey.io/announcement"
        vm_payload = {      "token": configure.VOICEMONKEY_TOKEN,
                            "text": message,
                            "device": device}
        response = await client.get(url, params = vm_payload) #headers = headers)
        print(response,"from voice monkey")


# Returns True - if our email is the one we are looking for
# Looking for VETs or VTOs from 'amazon'
def wanted_email(from_, subject):
    return ("amazon" in from_.lower() or configure.TEST_EMAIL_ALERTS) and \
            any(sub in subject for sub in configure.EMAIL_ALERT_SUBJECTS) and \
            "available" in subject

async def check_inbox():

    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(configure.IMAP_SERVER)
        mail.login(configure.EMAIL, configure.EMAIL_APP_PASSWORD)
        mail.select("inbox")  # Select the mailbox you want to use.

        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        if status == "OK":
            email_ids = messages[0].split()
            for email_id in email_ids:
                # Fetch the email by ID
                res, msg = mail.fetch(email_id, "(RFC822)")
                for response in msg:
                    if isinstance(response, tuple):
                        # Parse the email content
                        msg = email.message_from_bytes(response[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # Decode if needed
                            subject = subject.decode(encoding if encoding else "utf-8")

                        from_ = msg.get("From")
                        
                        # If the email has a body
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    body = part.get_payload(decode=True).decode()
                                    #print(f"Body: {body}")

                        else:
                            body = msg.get_payload(decode=True).decode()

                        email_msg = {
                            "body": body,
                            "from": from_,
                            "subject": subject,
                        }
                        print(email_msg)
                        lsub = subject.lower()
                        if (wanted_email(from_, lsub)):
                            msg = f'ALERT! ALERT! YOU HAVE {"VTO" if "vto" in lsub else "VET"} OPPORTUNITIES'
                            await voice_monkey(msg)
                            await notifyme_announce(msg)
        else:
            print("No new emails.")
        mail.logout()
    except Exception as e:
        print(f"Error: {e}")


async def email_watch_session(pause):
    try:
        # Call the function periodically
        #await voice_monkey()

        while True:
            await check_inbox()
            print(f"Waiting for {pause} seconds before checking again...")
            await asyncio.sleep(pause)  # Sleep for a few seconds.

    except Exception as e:
        print("-------------->", e, type(e), "<====================")



asyncio.run(email_watch_session(1))
