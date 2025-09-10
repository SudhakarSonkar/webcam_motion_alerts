
import smtplib
import mimetypes
import logging

from email.message import EmailMessage

# Configure logging
logging.basicConfig(
    filename="email_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

SENDER = RECEIVER = "sudhakar.sonkar07@gmail.com"
PASSWORD = "password"
def send_email(image_path):
    try:
        email_message = EmailMessage()
        email_message["Subject"] = "🚨 Motion Detected!"
        email_message["From"] = SENDER
        email_message["To"] = RECEIVER
        email_message.set_content("Hey, motion was detected. See attached image!")

        # Attach image
        mime_type, _ = mimetypes.guess_type(image_path)
        mime_type, mime_subtype = mime_type.split("/", 1)

        with open(image_path, "rb") as file:
            email_message.add_attachment(file.read(),
                                         maintype=mime_type,
                                         subtype=mime_subtype,
                                         filename=image_path)

        # Connect & send
        with smtplib.SMTP("smtp.gmail.com", 587) as gmail:
            gmail.ehlo()
            gmail.starttls()
            gmail.login(SENDER, PASSWORD)
            gmail.send_message(email_message)

        msg = f"✅ Email sent successfully with {image_path}"
        logging.info(msg)
        print(msg, flush=True)

    except Exception as e:
        msg = f"❌ Error sending email: {e}"
        logging.error(msg)
        print(msg, file=sys.stderr, flush=True)
