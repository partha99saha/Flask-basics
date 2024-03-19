import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_reset_password_email(email, reset_token):
    """
    Sends an email with a reset password link containing a token.

    Args:
        email (str): The recipient's email address.
        reset_token (str): The reset password token.

    Raises:
        Exception: If there's an error while sending the email.
    """
    sender_email = ""
    sender_password = ""
    smtp_mailbox = ""

    recipient_email = email

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset Your Password"
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # Create the HTML message with the reset token embedded in the link
    html = f"""
    <html>
      <body>
        <p>Click the following link to reset your password:</p>
        <p><a href="http://yourwebsite.com/reset_password?token={reset_token}">Reset Password</a></p>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    body = MIMEText(html, "html")

    # Attach parts into message container.
    msg.attach(body)

    # Send the message via SMTP server.
    try:
        with smtplib.SMTP(smtp_mailbox, 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        raise Exception("Failed to send reset password email.") from e
