import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Your Outlook email address and password
your_email = "achyutam.mehta@wonderbotz.com"
your_password = "Gj27aa0009"

# Email details
recipient_email = "achyutam.mehta@wonderbotz.com"
subject = "Test"
body = "Test."

# Setup the MIME
message = MIMEMultipart()
message['From'] = your_email
message['To'] = recipient_email
message['Subject'] = subject
message.attach(MIMEText(body, 'plain'))

# Establish a secure session with Outlook's SMTP server
try:
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()  
        server.login(your_email, your_password) 
        text = message.as_string()
        server.sendmail(your_email, recipient_email, text)
        print("Email sent successfully")
except Exception as e:
    print(f"Error: {e}")
