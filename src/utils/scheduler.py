import pytz
import schedule
import time

def run_daily_digest():
    # Call the function that generates and sends the email here
    pass

# Convert the desired timezone to a pytz timezone object
pacific_tz = pytz.timezone('America/Los_Angeles')

# Schedule the function to run every day at 7:30 AM Pacific time
schedule.every().day.at('07:30').do(run_daily_digest).in_timezone(pacific_tz)

# Keep the script running to allow the scheduled jobs to execute
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait for 60 seconds before checking the schedule again
