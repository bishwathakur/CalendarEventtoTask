# Google Calendar to Google Tasks Automation

This Python script automates the process of fetching today's events from Google Calendar and creating corresponding tasks in Google Tasks. It uses the Google Calendar API and Google Tasks API for interaction with the respective services.

## Prerequisites:

1. Python 3.x installed on your system.
2. Google account with access to Google Calendar and Google Tasks.
3. credentials.json: OAuth 2.0 client credentials file obtained from the Google Cloud Console.
4. token.json: Authorization token file generated during the OAuth 2.0 authorization process.


## Installation:

Clone this repository to your local machine:

```
git clone https://github.com/your-username/google-calendar-tasks-automation.git
```
Navigate to the project directory:

```
cd google-calendar-tasks-automation
```

Install the required Python packages:

```
pip install -r requirements.txt
```
Place your credentials.json file in the project directory.

## Usage
Ensure that your credentials.json file and token.json file (if available) are in the project directory.

## Run the Python script:

```
python main.py
```
The script will fetch today's events from your primary Google Calendar, save them in a JSON file (eventsOf_{date}.json), and create corresponding tasks in your Google Tasks.

## Scheduled Execution
You can schedule the script to run daily using cron (on Unix-like systems) or Task Scheduler (on Windows). Follow the instructions in the respective sections below to set up scheduled execution.

## Using Task Scheduler (Windows)
Open Task Scheduler and create a new basic task.
Follow the wizard to schedule the task, specifying the script (main.py) as the program to run.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

