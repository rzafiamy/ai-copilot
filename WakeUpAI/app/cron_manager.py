import schedule
import time

def send_content(email, content):
    print(f"Sending content to {email}: {content}")

def schedule_email(email, content, time_of_day):
    schedule.every().day.at(time_of_day).do(send_content, email=email, content=content)

def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)
