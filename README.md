# GCalpy

This is a script that can be used to get the next calendar event on a calendar, and open the associated virtual meeting if it is attached

## Install

Create a virtualenv

`mkvirtualenv gcalpy`

Install requirements

`pip install -r requirements.txt`

Create an Automator script that runs the shell script run.sh

```
source ~/.virtualenvs/gcalpy/bin/activate
cd /<path>/gcalpy
python run.py
```

## Setup API Credentials

1. Goto https://developers.google.com/calendar/quickstart/python
2. Click "Enable the google calendar API"


## Bonus! Triggering from Alexa (OSx solution)

Tie into Folder Actions on OSx..

```applescript
property dialog_timeout : 30 -- set the amount of time before dialogs auto-answer.

on adding folder items to this_folder after receiving added_items
    try
        tell application "Finder"
            --get the name of the folder
            set the folder_name to the name of this_folder
        end tell

        set the_script to "source ~/.virtualenvs/gcalpy/bin/activate; cd /git/gcalpy; python run.py"
        set the_result to do shell script the_script
        display dialog the_result giving up after dialog_timeout
    end try
end adding folder items to
```

## Other tools like this

https://github.com/benbalter/zoom-go
