import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email_credentials, recipient, subject, email_content):
    try:
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = email_credentials["sender_mail"]
        msg['To'] = recipient

        # Create the HTML and plain-text parts of the message.
        html = email_content
        text = email_content

        # Turn these into plain/html MIMEText objects and add them to the MIMEMultipart message.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Create SMTP object for sending the email.
        smtp_obj = smtplib.SMTP(email_credentials["mail_server"], int(email_credentials["mail_port"]))
        smtp_obj.ehlo()

        if email_credentials["mail_use_tls"] == 'True':
            smtp_obj.starttls()

        smtp_obj.login(email_credentials["sender_mail"], email_credentials["sender_pass"])
        smtp_obj.sendmail(email_credentials["sender_mail"], recipient, msg.as_string())
        smtp_obj.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error: {}".format(str(e)))
