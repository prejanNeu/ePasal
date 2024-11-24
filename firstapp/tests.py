from django.test import TestCase
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('ePasal.2024@gmail.com', 'thenewPasal@123')
print("Login successful!")
server.quit()
