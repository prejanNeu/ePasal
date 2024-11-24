import random 
import string
from django.core.mail import send_mail
from django.conf import settings

def generateOtp():
    length = 6
    characters = "0123456789"
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp 


def sendEmail(email_id,otp):
    email=email_id
    subject = "Verify Your Email Address for ePasal"
    message = f"Dear User,\n\tThank you for registering with ePasal! Use the OTP below to verify your email address:OTP: {otp} \n\nIf you did not register on ePasal, please ignore this email.\nBest regards,\nePasal Team"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


