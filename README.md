# Bug Diary

A command-line Python app that logs the errors you hit while learning, so you can search past fixes and see which mistakes you repeat most.

## Features
- Log a bug with its error type, topic, what happened and the fix
- View all bugs
- Search by keyword (type, topic, description and fix)
- Statistics: bugs by type, most repeated mistake, trickiest topic, bugs in the last 7 days
- Delete a bug, with a y/n confirmation
- Data saved automatically to a CSV file

## Run it
Requires Python 3. No packages to install.

    python bug_diary.py

Choose an option from the menu with a number from 1 to 5, or 0 to exit.

## Built with
Python standard library only: `csv` and `datetime`.

## Ideas for next steps
- Edit existing entries
- Move storage to SQLite
- Add automated tests