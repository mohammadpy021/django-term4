from celery import shared_task
import time

@shared_task
def send_welcome_email_task(user_email):
    # Simulate a time-consuming task like sending an email
    print(f"Starting to send welcome email to {user_email}...")
    
    time.sleep(5) # Delay for 5 seconds to simulate network latency
    
    # In a real project, you would use django.core.mail.send_mail here
    print(f"Successfully sent welcome email to {user_email}!")
    
    return True