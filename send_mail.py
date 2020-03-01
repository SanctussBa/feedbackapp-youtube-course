import smtplib
from email.mime.text import MIMEText


def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '643f731f503503'
    password = '93137d7fc43e67'
    message = "<h3>New Feedback Submission</h3><ul><li>Customer: {}</li><li>Dealer: {}</li><li>Rating: {}</li><li>Comments: {}</li></ul>".format(customer, dealer, rating, comments)

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
