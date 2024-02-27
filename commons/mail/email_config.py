import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .email_template import signup_content, login_content,consultation_content, waiting_for_approval_content, ready_for_dispatch_content, dispatched_content


def send_email(subject, body, recipients):
    sender = "customercare@fcomindia.com"
    password = "Fcom@123"
    #testmsg
    # msg = MIMEText(body)
    # html msg
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, "html"))
    # end html msg
    msg['Subject'] = subject
    msg['From'] = "customercare@fcomindia.com"
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


def signup_mail_otp(otp, mailto ):
    subject = "FCOM Registeration - One-Time Password"
    body = signup_content(otp)
    recipients = [mailto]
    send_email(subject, body, recipients)

def login_mail_otp(otp, mailto, customer_name ):
    subject = "FCOM Login - One-Time Password"
    body = login_content(customer_name, otp)
    recipients = [mailto]
    send_email(subject, body, recipients)

def send_consultation_msg(customer_name, consultation_date, mailto):
    subject = "FCOM Designer Visiting Date"
    body = consultation_content(customer_name, consultation_date)
    recipients = [mailto]
    send_email(subject, body, recipients)



def send_order_waiting_for_approval_msg(customer_name, order_id, mailto ):
    subject = "FCOM Order Confirmation"
    body = waiting_for_approval_content(customer_name, order_id)
    recipients = [mailto]
    send_email(subject, body, recipients)

def send_order_ready_for_dispatch_msg(customer_name, delivery_date, order_id, mailto ):
    subject = "FCOM Order Ready for dispatch "
    body = ready_for_dispatch_content(customer_name, order_id, delivery_date)
    recipients = [mailto]
    send_email(subject, body, recipients)

def send_order_dispatched_msg(customer_name, order_id, mailto ):
    subject = "FCOM Order is Dispatched "
    body = dispatched_content(customer_name, order_id)
    recipients = [mailto]
    send_email(subject, body, recipients)


def contactmessage(name, mobile, message):
    subject = "Customer Enquiry"
    body = f' Name: {name}, Mobile No: {mobile}, Message: {message}.'
    recipients = ['customercare@fcomindia.com']
    send_email(subject, body, recipients)